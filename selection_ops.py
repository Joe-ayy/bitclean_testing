#region ### Imports ###
import list_ops as l_ops
import pixel_ops as p_ops
import object_stats as o_stats
from copy import deepcopy
#endregion


class StoreObject:
    # The objects in this class are objects found in a store map, they will either be determined to be a structure or
    # dust (something not actually present in the store)
    def __init__(self, data, img_width, object_type=None):
        # Create a list to hold all the pixels that belong to this StoreObject
        self.pixels_in_obj = data

        # Create an object type
        self.obj_type = object_type

        # Create and set the pixel at the top, bottom, left, and right most parts of the object
        self.top_pixel = None
        self.bot_pixel = None
        self.left_pixel = None
        self.right_pixel = None
        self.set_boundary_pixels(img_width)

        # Create and set object's absolute width and height
        self.abs_height = None
        self.abs_width = None
        self.set_width_and_height()

        # Create and set object's bounding box size
        self.bbox_size = None
        self.set_bbox_size()

        # Create and set pixel rows and columns of object
        self.pixel_rows_in_obj = []
        self.generate_pixel_rows_in_obj()
        self.pixel_cols_in_obj = []
        self.generate_pixel_columns_in_obj()

        # Create pixel densities for each row and column
        self.pixel_density_row = []
        self.pixel_density_col = []

        # Create weighted pixel densities for each row and column (Pixel density per row/col * average hue value for
        # each row and column
        self.weighted_pixel_density_row = []
        self.weighted_pixel_density_col = []

    # region ### Functions to set values ###
    # region ### Functions to initialize values ###
    def set_boundary_pixels(self, width):
        # Get the top most, bottom most, left most, and right most pixels of the object and return the appropriate
        # row and column values to determine the bounding box for the object

        # region ### Get the top most pixel ###
        # Since the lists are order by absolute id, the first pixel in the list will be either the top most pixel or one
        # of the top most pixels
        self.top_pixel = self.pixels_in_obj[0]
        #endregion

        # region ### Get the bottom most pixel ###
        # Since the lists are order by absolute id, the last pixel in the list will be either the bottom most pixel or
        # one of the bottom most pixels
        self.bot_pixel = self.pixels_in_obj[-1]
        #endregion

        # region ### Get the left most pixel ###
        # In order to find the left most pixel, we have to find the smallest remainder of modular division of the
        # absolute id mod the width of the image

        # Initialize a value to hold the reference to the index of the pixel that is left most
        self.left_pixel = self.pixels_in_obj[0]

        # Iterate through the entire object, updating the index as the left most pixel is found
        for i in range(len(self.pixels_in_obj) - 1):
            # Check the distance from the left
            next_pixel = self.pixels_in_obj[i + 1]

            if (next_pixel.gid % width) < (self.left_pixel.gid % width):
                self.left_pixel = next_pixel
        #endregion

        # region ### Get the right most pixel ###
        # In order to find the right most pixel, we have to find the largest remainder of modular division of the
        # absolute id mod the width of the image

        # Initialize a value to hold the reference to the index of the pixel that is the right most
        self.right_pixel = self.pixels_in_obj[0]

        # Iterate through the entire object, updating the index as the right most pixel is found
        for j in range(len(self.pixels_in_obj) - 1):
            # Check the distance from the right
            next_pixel = self.pixels_in_obj[j + 1]

            if (next_pixel.gid % width) > (self.right_pixel.gid % width):
                self.right_pixel = next_pixel
        #endregion

    def set_width_and_height(self):
        # Width
        self.abs_width = self.right_pixel.pixel_col_id - self.left_pixel.pixel_col_id + 1
        # Height
        self.abs_height = self.bot_pixel.pixel_row_id - self.top_pixel.pixel_row_id + 1

    def set_bbox_size(self):
        # Set the size of the bounding box for the object
        self.bbox_size = self.abs_width * self.abs_height

    def generate_pixel_rows_in_obj(self):
        # Initialize temporary row
        temp_row = []

        # Iterate through each row, checking the pixel against the row of the top most pixel plus the row offset
        for i in range(self.abs_height):
            for j in range(len(self.pixels_in_obj)):
                if self.pixels_in_obj[j].pixel_row_id == self.top_pixel.pixel_row_id + i:
                    temp_row.append(self.pixels_in_obj[j])

            # For each row, add the row of pixels to the list
            self.pixel_rows_in_obj.append(deepcopy(temp_row))
            # Clear the temp list
            temp_row.clear()

    def generate_pixel_columns_in_obj(self):
        # Initialize temporary column
        temp_col = []

        # Iterate through each column, checking the pixel against the column of the left most pixel plus the column
        # offset
        for i in range(self.abs_width):
            for j in range(len(self.pixels_in_obj)):
                if self.pixels_in_obj[j].pixel_col_id == self.left_pixel.pixel_col_id + i:
                    temp_col.append(self.pixels_in_obj[j])

            # For each column, add the column of pixels to the list
            self.pixel_cols_in_obj.append(deepcopy(temp_col))
            # Clear the temp list
            temp_col.clear()

    def set_pixel_densities(self):
        # Set the pixel densities for the rows
        for i in range(len(self.pixel_rows_in_obj)):
            # Get the number of pixels in a row
            num_pixels = len(self.pixel_rows_in_obj[i])
            # Get the pixel density for the row
            pixel_density = num_pixels / self.abs_width
            # Set the pixel density for the row
            self.pixel_density_row.append(pixel_density)

        # Set the pixel densities for the columns
        for j in range(len(self.pixel_cols_in_obj)):
            # Get the number of pixels in a column
            num_pixels = len(self.pixel_cols_in_obj[j])
            # Get the pixel density for the column
            pixel_density = num_pixels / self.abs_height
            # Set the pixel density for the column
            self.pixel_density_col.append(pixel_density)

    def set_weighted_pixel_densities(self):
        # Set the weighted pixel densities for the rows
        for i in range(len(self.pixel_density_row)):
            # Get the average hue of the row
            avg_hue = o_stats.get_avg_hue_of_row_or_col(self.pixel_rows_in_obj[i])
            # Calculate the weighted pixel density for the row
            weighted_pixel_density = avg_hue * self.pixel_density_row[i]
            # Set the weighted pixel density for each row
            self.weighted_pixel_density_row.append(weighted_pixel_density)

        # Set the weighted pixel densities for the columns
        for j in range(len(self.pixel_density_col)):
            # Get the average hue of the column
            avg_hue = o_stats.get_avg_hue_of_row_or_col(self.pixel_cols_in_obj[j])
            # Calculate the weighted pixel density for each column
            weighted_pixel_density = avg_hue * self.pixel_density_col[j]
            # Set the weighted pixel density for each column
            self.weighted_pixel_density_col.append(weighted_pixel_density)

    #endregion

    def update_object_type(self, object_type):
        self.obj_type = object_type
    #endregion

    def print_width_and_height_to_console(self):
        print("Absolute object width:", self.abs_width, "Absolute object height:", self.abs_height)


class StoreMap:
    def __init__(self, pixels, img_w, img_h):
        # Initialize values
        self.pixel_matrix = pixels
        self.img_width = img_w
        self.img_height = img_h
        self.objects_in_store = []

        # Temporarily store a list of all pixels found per object
        self.found_pixels = []

        # Temporarily store a list of all pixels connected to the root node pixel via other pixel nodes
        self.storage_pixels = []

        # Temporarily store a list of all adjacent pixels found per pixel
        self.adj_pixels = []

        # Generate list of objects in the store upon creation
        self.find_objects_in_store()

        # Add the bounding box mask functionality for visual bounding boxes upon file creation
        self.transform_bbox_pixels()

    def find_objects_in_store(self):
        # Iterate through the list of pixels to find objects in the store
        # These objects will be the non-white pixels connected to 0 or more non-white pixels and are to be determined
        # in the future to be either a structure present in the store or dust
        for i in range(self.img_height):
            for j in range(self.img_width):
                # First, check if the pixel being accessed is white
                if self.pixel_matrix[i][j].all_colors == p_ops.all_white:
                    # Set the pixel to being touched
                    self.pixel_matrix[i][j].touched = True
                    continue
                else:  # This is if the pixel is non-white
                    # Next, check if the pixel is touched
                    if self.pixel_matrix[i][j].touched:
                        continue
                    else:  # This is if the pixel has not been touched
                        # Set the pixel to be touched
                        self.pixel_matrix[i][j].touched = True

                        # Create a list for a StoreObject and add the pixel as the first entry
                        object_in_store = [self.pixel_matrix[i][j]]

                        # Find the adjacent connections to the node pixel
                        control = self.discover_connections(i, j)

                        # Loop through all the pixels until the entire object is captured
                        while control:
                            control = self.evaluate_connections()

                        for k in range(len(self.found_pixels)):
                            l_ops.insort_pixels(object_in_store, self.found_pixels[k])

                        # Empty the temporary found_pixels list
                        self.found_pixels.clear()

                        # Add this object to the store_objects list
                        self.objects_in_store.append(StoreObject(object_in_store, self.img_width))

    def discover_connections(self, row_index, col_index):
        # Initialize a boolean to determine if any connections were discovered
        discovered = False

        # Find all the neighboring pixels to the originally found pixel
        # Find any adjacent pixels that are non-white and not touched using this diagram
        # TL TM TR - Top Left, Top Middle, Top Right
        # CL XX CR - Center Left, XX is Current Pixel, Center Right
        # BL BM BR - Bottom Left, Bottom Middle, Bottom Right

        #region ### TOP PIXELS: Only check the top pixels if a row above the current one exists ###
        if row_index > 0:
            # Set the top middle pixel's row and column
            tm_row = row_index - 1
            tm_col = col_index
            # Add the pixel to the adjacent pixel list if not touched
            if not self.pixel_matrix[tm_row][tm_col].touched:
                self.adj_pixels.append(self.pixel_matrix[tm_row][tm_col])
                discovered = True

            if col_index != 0:
                # Set the top left pixel's row and column
                tl_row = row_index - 1
                tl_col = col_index - 1
                # Add the pixel to the adjacent pixel list if not touched
                if not self.pixel_matrix[tl_row][tl_col].touched:
                    self.adj_pixels.append(self.pixel_matrix[tl_row][tl_col])
                    discovered = True

            if col_index != (self.img_width - 1):
                # Set the top right pixel's row and column
                tr_row = row_index - 1
                tr_col = col_index + 1
                # Add the pixel to the adjacent pixel list if not touched
                if not self.pixel_matrix[tr_row][tr_col].touched:
                    self.adj_pixels.append(self.pixel_matrix[tr_row][tr_col])
                    discovered = True
        #endregion

        # region ### LEFT/RIGHT PIXELS: Only check the left and right pixels if they exist ###
        if col_index != 0:
            # Set the center left pixel's row and column
            cl_row = row_index
            cl_col = col_index - 1
            # Add the pixel to the adjacent pixel list if not touched
            if not self.pixel_matrix[cl_row][cl_col].touched:
                self.adj_pixels.append(self.pixel_matrix[cl_row][cl_col])
                discovered = True

        if col_index != (self.img_width - 1):
            # Set the center right pixel's row and column
            cr_row = row_index
            cr_col = col_index + 1
            # Add the pixel to the adjacent pixel list if not touched
            if not self.pixel_matrix[cr_row][cr_col].touched:
                self.adj_pixels.append(self.pixel_matrix[cr_row][cr_col])
                discovered = True
        #endregion

        # region ### BOTTOM PIXELS: Check the bottom pixels if a row below them exists ###
        if row_index < self.img_height - 1:
            # Set the bottom middle pixel's row and column
            bm_row = row_index + 1
            bm_col = col_index
            # Add the pixel to the adjacent pixel list if not touched
            if not self.pixel_matrix[bm_row][bm_col].touched:
                self.adj_pixels.append(self.pixel_matrix[bm_row][bm_col])
                discovered = True

            if col_index != 0:
                # Set the bottom left pixel's row and column
                bl_row = row_index + 1
                bl_col = col_index - 1
                # Add the pixel to the adjacent pixel list if not touched
                if not self.pixel_matrix[bl_row][bl_col].touched:
                    self.adj_pixels.append(self.pixel_matrix[bl_row][bl_col])
                    discovered = True

            if col_index != (self.img_width - 1):
                # Set the bottom right pixel's row and column
                br_row = row_index + 1
                br_col = col_index + 1
                # Add the pixel to the adjacent pixel list if not touched
                if not self.pixel_matrix[br_row][br_col].touched:
                    self.adj_pixels.append(self.pixel_matrix[br_row][br_col])
                    discovered = True
        #endregion

        return discovered

    def evaluate_connections(self):
        # Iterate through the found adjacent pixels and add them to storage to be processed
        for i in range(len(self.adj_pixels)):
            if self.adj_pixels[i].all_colors == p_ops.all_white:
                self.adj_pixels[i].touched = True
            elif not self.adj_pixels[i].touched:
                self.adj_pixels[i].touched = True
                self.storage_pixels.append(self.adj_pixels[i])

        # Clean out the adjacent pixel list
        self.adj_pixels.clear()

        # Work on the first pixel in storage - pixels in storage have been touched and are used to continue searching
        # for additional neighboring pixels
        first_storage_pixel_abs_value = None

        if len(self.storage_pixels) != 0:
            self.found_pixels.append(self.storage_pixels[0])
            first_storage_pixel_abs_value = self.storage_pixels[0].gid

        # Remove the pixel from storage
        self.storage_pixels = self.storage_pixels[1:]

        # Discover any connections to this pixel, if they are valid, add them to the storage list
        if first_storage_pixel_abs_value is not None:
            row, col = p_ops.get_row_and_col(first_storage_pixel_abs_value, self.img_width)
            self.discover_connections(row, col)
            return True
        else:
            return False

    def print_all_objects_width_and_height_to_console(self):
        for i in range(len(self.objects_in_store)):
            self.objects_in_store[i].print_width_and_height_to_console()

    def transform_bbox_pixels(self):
        # We will utilize a mask to draw bounding boxes on each and every object in the image
        # The constraints for the bounding boxes are the rows and columns of the top most, bottom most, left most, and
        # right most pixels

        # Set the black color
        black = [0, 0, 0]

        #region ### Draw the box for each object ###
        # Iterate through all the objects in the store
        for i in range(len(self.objects_in_store)):
            # Get the top pixel row
            top_pixel_row = self.objects_in_store[i].top_pixel.pixel_row_id
            # Get the bottom pixel row
            bot_pixel_row = self.objects_in_store[i].bot_pixel.pixel_row_id
            # Get the left pixel column
            left_pixel_col = self.objects_in_store[i].left_pixel.pixel_col_id
            # Get the right pixel column
            right_pixel_col = self.objects_in_store[i].right_pixel.pixel_col_id

            # Draw the top and bottom of the box
            for j in range(self.objects_in_store[i].abs_width):
                self.pixel_matrix[top_pixel_row][left_pixel_col + j].bbox_mask = black
                self.pixel_matrix[bot_pixel_row][left_pixel_col + j].bbox_mask = black

            # Draw the left and right of the box
            for k in range(self.objects_in_store[i].abs_height):
                self.pixel_matrix[top_pixel_row + k][left_pixel_col].bbox_mask = black
                self.pixel_matrix[top_pixel_row + k][right_pixel_col].bbox_mask = black

    def set_pixel_densities_of_objects(self):
        # Set the densities of the pixels in each object
        for i in range(len(self.objects_in_store)):
            self.objects_in_store[i].set_densities()

    def set_hues_for_file_output(self):
        # Set the hues for each object for file output
        for i in range(len(self.objects_in_store)):
            o_stats.get_avg_hue_object(self.objects_in_store[i], "tuple")
