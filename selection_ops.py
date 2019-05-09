#region ### Imports ###
import tree_ops as t_ops
import list_ops as l_ops
import pixel_ops as p_ops
#endregion


class StoreObject:
    # The objects in this class are objects found in a store map, they will either be determined to be a structure or
    # dust (something not actually present in the store)
    def __init__(self, data, object_type=None):
        # Create a list to hold all the pixels that belong to this StoreObject
        self.pixels_in_obj = data

        # Create an object type
        self.obj_type = object_type

        # Get the pixel at the top, bottom, left, and right most parts of the object
        self.top_pixel = None
        self.bot_pixel = None
        self.left_pixel = None
        self.right_pixel = None

        # Create object's absolute width and height
        self.abs_height = None
        self.abs_width = None

    def update_object_type(self, object_type):
        self.obj_type = object_type

    def set_bbox_and_abs_width_height(self, width):
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

        # Also set the width and height
        self.set_width_and_height()

    def set_width_and_height(self):
        # Width
        self.abs_width = self.right_pixel.pixel_col_id - self.left_pixel.pixel_col_id + 1

        # Height
        self.abs_height = self.bot_pixel.pixel_row_id - self.top_pixel.pixel_row_id + 1

    def print_width_and_height_to_console(self):
        print("Absolute object width:", self.abs_width, "Absolute object height:", self.abs_height)


class StoreMap:
    def __init__(self, pixels, img_w, img_h, pixel_matrix=[]):
        # Initialize values
        self.all_pixels = pixels
        self.all_pixel_matrix = pixel_matrix
        self.bbox_mask = pixels.copy()
        self.img_width = img_w
        self.img_height = img_h
        self.objects_in_store = None

        # Temporarily store a list of all pixels found per object
        self.found_pixels = []

        # Temporarily store a list of all pixels connected to the root node pixel via other pixel nodes
        self.storage_pixels = []

        # Temporarily store a list of all adjacent pixels found per pixel
        self.adj_pixels = []

        # Generate list of objects in the store upon creation
        self.find_objects_in_store()

        # Set the bounding boxes of each object
        self.set_bounding_boxes()

    def find_objects_in_store(self):
        # Return list containing all the found objects
        store_objects = []

        # Iterate through the list of pixels to find objects in the store
        # These objects will be the non-white pixels connected to 0 or more non-white pixels and are to be determined
        # in the future to be either a structure present in the store or dust
        for i in range(len(self.all_pixels)):
            # First, check if the pixel being accessed is white
            if self.all_pixels[i].all_colors == p_ops.all_white:
                # Set the pixel to being touched
                self.all_pixels[i].touched = True
                continue
            else:  # This is if the pixel is non-white
                # Next, check if the pixel is touched
                if self.all_pixels[i].touched:
                    continue
                else:  # This is if the pixel has not been touched
                    # Set the pixel to be touched
                    self.all_pixels[i].touched = True

                    # Create a list for a StoreObject and add the pixel as the first entry
                    object_in_store = [self.all_pixels[i]]

                    # Find the adjacent connections to the node pixel
                    control = self.discover_connections(i)

                    # Loop through all the pixels until the entire object is captured
                    while control:
                        control = self.evaluate_connections()

                    for j in range(len(self.found_pixels)):
                        l_ops.insort_pixels(object_in_store, self.found_pixels[j])

                    # Empty the temporary found_pixels list
                    self.found_pixels.clear()

                    # Add this object to the store_objects list
                    store_objects.append(StoreObject(object_in_store))

        self.objects_in_store = store_objects.copy()

    def discover_connections(self, index):
        # Initialize a boolean to determine if any connections were discovered
        discovered = False

        # Find all the neighboring pixels to the originally found pixel
        # Find any adjacent pixels that are non-white and not touched using this diagram
        # TL TM TR - Top Left, Top Middle, Top Right
        # CL XX CR - Center Left, XX is Current Pixel, Center Right
        # BL BM BR - Bottom Left, Bottom Middle, Bottom Right

        #region ### TOP PIXELS: Only check the top pixels if a row above the current one exists ###
        if index > self.img_width:
            tm_pixel = [self.all_pixels[index].pixel_row_id - 1, self.all_pixels[index].pixel_col_id]

            # Find the absolute id, use this to check if the pixel has been touched already
            abs_id = p_ops.get_pixel_gid_by_row_col(tm_pixel[0], tm_pixel[1], self.img_width)

            if not self.all_pixels[abs_id].touched:
                self.adj_pixels.append(abs_id)
                discovered = True

            if index % self.img_width != 0:
                tl_pixel = [self.all_pixels[index].pixel_row_id - 1, self.all_pixels[index].pixel_col_id - 1]

                # Find the absolute id, use this to check if the pixel has been touched already
                abs_id = p_ops.get_pixel_gid_by_row_col(tl_pixel[0], tl_pixel[1], self.img_width)

                if not self.all_pixels[abs_id].touched:
                    self.adj_pixels.append(abs_id)
                    discovered = True

            if (index + 1) % self.img_width != 0:
                tr_pixel = [self.all_pixels[index].pixel_row_id - 1, self.all_pixels[index].pixel_col_id + 1]

                # Find the absolute id, use this to check if the pixel has been touched already
                abs_id = p_ops.get_pixel_gid_by_row_col(tr_pixel[0], tr_pixel[1], self.img_width)

                if not self.all_pixels[abs_id].touched:
                    self.adj_pixels.append(abs_id)
                    discovered = True
        #endregion

        # region ### LEFT/RIGHT PIXELS: Only check the left and right pixels if they exist ###
        if index % self.img_width != 0:
            cl_pixel = [self.all_pixels[index].pixel_row_id, self.all_pixels[index].pixel_col_id - 1]

            # Find the absolute id, use this to check if the pixel has been touched already
            abs_id = p_ops.get_pixel_gid_by_row_col(cl_pixel[0], cl_pixel[1], self.img_width)

            if not self.all_pixels[abs_id].touched:
                self.adj_pixels.append(abs_id)
                discovered = True

        if (index + 1) % self.img_width != 0:
            cr_pixel = [self.all_pixels[index].pixel_row_id, self.all_pixels[index].pixel_col_id + 1]

            # Find the absolute id, use this to check if the pixel has been touched already
            abs_id = p_ops.get_pixel_gid_by_row_col(cr_pixel[0], cr_pixel[1], self.img_width)

            if not self.all_pixels[abs_id].touched:
                self.adj_pixels.append(abs_id)
                discovered = True
        #endregion

        # region ### BOTTOM PIXELS: Check the bottom pixels if a row below them exists ###
        bm_pixel = [self.all_pixels[index].pixel_row_id + 1, self.all_pixels[index].pixel_col_id]

        # Find the absolute id, use this to check if the pixel has been touched already
        abs_id = p_ops.get_pixel_gid_by_row_col(bm_pixel[0], bm_pixel[1], self.img_width)

        if abs_id < (self.img_width * self.img_height):
            if not self.all_pixels[abs_id].touched:
                self.adj_pixels.append(abs_id)
                discovered = True

            if index % self.img_width != 0:
                bl_pixel = [self.all_pixels[index].pixel_row_id + 1, self.all_pixels[index].pixel_col_id - 1]

                # Find the absolute id, use this to check if the pixel has been touched already
                abs_id = p_ops.get_pixel_gid_by_row_col(bl_pixel[0], bl_pixel[1], self.img_width)

                if not self.all_pixels[abs_id].touched:
                    self.adj_pixels.append(abs_id)
                    discovered = True

            if index != (self.img_width * self.img_height - 1):
                br_pixel = [self.all_pixels[index].pixel_row_id + 1, self.all_pixels[index].pixel_col_id + 1]

                # Find the absolute id, use this to check if the pixel has been touched already
                abs_id = p_ops.get_pixel_gid_by_row_col(br_pixel[0], br_pixel[1], self.img_width)

                if abs_id != self.img_width * self.img_height:
                    if not self.all_pixels[abs_id].touched:
                        self.adj_pixels.append(abs_id)
                        discovered = True
        #endregion

        return discovered

    def evaluate_connections(self):
        # Iterate through the found adjacent pixels and add them to storage to be processed
        for i in range(len(self.adj_pixels)):
            if self.all_pixels[self.adj_pixels[i]].all_colors == p_ops.all_white:
                self.all_pixels[self.adj_pixels[i]].touched = True
            elif not self.all_pixels[self.adj_pixels[i]].touched:
                self.all_pixels[self.adj_pixels[i]].touched = True
                self.storage_pixels.append(self.all_pixels[self.adj_pixels[i]])

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
            self.discover_connections(first_storage_pixel_abs_value)
            return True
        else:
            return False

    def set_bounding_boxes(self):
        for i in range(len(self.objects_in_store)):
            self.objects_in_store[i].set_bbox_and_abs_width_height(self.img_width)

    def print_all_objects_width_and_height_to_console(self):
        for i in range(len(self.objects_in_store)):
            self.objects_in_store[i].print_width_and_height_to_console()

    def transform_bbox_pixels(self):
        # We will utilize a mask to draw bounding boxes on each and every object in the image
        # The constraints for the bounding boxes are the rows and columns of the top most, bottom most, left most, and
        # right most pixels

        # Set the black color
        black = [0, 0, 0]

        # Draw the box for each object
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

            # Get the global id of the top left pixel
            tl_pixel_gid = p_ops.get_pixel_gid_by_row_col(top_pixel_row, left_pixel_col, self.img_width)
            # Get the global id of the bottom left pixel
            bl_pixel_gid = p_ops.get_pixel_gid_by_row_col(bot_pixel_row, left_pixel_col, self.img_width)
            # Get the global id of the top right pixel
            tr_pixel_gid = p_ops.get_pixel_gid_by_row_col(top_pixel_row, right_pixel_col, self.img_width)

            # Draw the top and bottom of the box
            for j in range(self.objects_in_store[i].abs_width):
                self.bbox_mask[tl_pixel_gid + j].rgb_colors = black
                self.bbox_mask[bl_pixel_gid + j].rgb_colors = black

            # Draw the left and right of the box
            for k in range(self.objects_in_store[i].abs_height):
                self.bbox_mask[tl_pixel_gid + k * self.img_width].rgb_colors = black
                self.bbox_mask[tr_pixel_gid + k * self.img_width].rgb_colors = black
