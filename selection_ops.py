#region ### Imports ###
import tree_ops as t_ops
import list_ops as l_ops
import pixel_ops as p_ops
#endregion


class StoreObject:
    # The objects in this class are objects found in a store map, they will either be determined to be a structure or
    # dust (something not actually present in the store)

    object_type = None  # This will either be set to "structure" or "dust"
    selection = []      # Sorted list, by absolute id, that will hold all the pixels of the object

    def __init__(self, data):
        # Create a binary tree to hold all the pixels that belong to this StoreObject
        self.selection.append(data)


class StoreMap:
    # Temporarily store a list of all pixels found per object
    found_pixels = []

    # Temporarily store a list of all pixels connected to the root node pixel via other pixel nodes
    storage_pixels = []

    # Temporarily store a list of all adjacent pixels found per pixel
    adj_pixels = []

    def __init__(self, pixels, img_w, img_h):
        self.pixel_list = pixels
        self.width = img_w
        self.height = img_h

    def find_objects_in_store(self):
        # Return list containing all the found objects
        store_objects = []

        # Iterate through the list of pixels to find objects in the store
        # These objects will be the non-white pixels connected to 0 or more non-white pixels and are to be determined
        # in the future to be either a structure present in the store or dust
        for i in range(len(self.pixel_list)):
            # First, check if the pixel being accessed is white
            if self.pixel_list[i].all_colors == p_ops.all_white:
                # Set the pixel to being touched
                self.pixel_list[i].touched = True
                continue
            else:  # This is if the pixel is non-white
                # Next, check if the pixel is touched
                if self.pixel_list[i].touched:
                    continue
                else:  # This is if the pixel has not been touched
                    # Set the pixel to be touched
                    self.pixel_list[i].touched = True

                    # Create a StoreObject and add the pixel as the root node
                    object_in_store = StoreObject(self.pixel_list[i].global_id)

                    # Find the adjacent connections to the node pixel
                    control = self.discover_connections(i)

                    # Loop through all the pixels until the entire object is captured
                    while control:
                        control = self.evaluate_connections()

                    for j in range(len(self.found_pixels)):
                        l_ops.insort_pixels(object_in_store.selection, self.found_pixels[j])

                    # Empty the temporary found_pixels list
                    self.found_pixels.clear()

                    # Add this object to the store_objects list
                    store_objects.append(object_in_store)

        return store_objects

    def discover_connections(self, index):
        # Initialize a boolean to determine if any connections were discovered
        discovered = False

        # Find all the neighboring pixels to the originally found pixel

        # Find any adjacent pixels that are non-white and not touched using this diagram
        # TL TM TR - Top Left, Top Middle, Top Right
        # CL XX CR - Center Left, XX is Current Pixel, Center Right
        # BL BM BR - Bottom Left, Bottom Middle, Bottom Right

        # Only check the top pixels if a row above the current one exists
        if index > self.width:
            #                       Row                            Column
            tm_pixel = [self.pixel_list[index].pix_row_id - 1, self.pixel_list[index].pix_col_id]

            # Find the absolute id, use this to check if the pixel has been touched already
            abs_id = p_ops.get_pixel_by_row_col(tm_pixel[0], tm_pixel[1], self.width)

            if not self.pixel_list[abs_id].touched:
                self.adj_pixels.append(abs_id)
                discovered = True

            if index % self.width != 0:
                #                       Row                            Column
                tl_pixel = [self.pixel_list[index].pix_row_id - 1, self.pixel_list[index].pix_col_id - 1]

                # Find the absolute id, use this to check if the pixel has been touched already
                abs_id = p_ops.get_pixel_by_row_col(tl_pixel[0], tl_pixel[1], self.width)

                if not self.pixel_list[abs_id].touched:
                    self.adj_pixels.append(abs_id)
                    discovered = True

            if (index + 1) % self.width != 0:
                #                       Row                            Column
                tr_pixel = [self.pixel_list[index].pix_row_id - 1, self.pixel_list[index].pix_col_id + 1]

                # Find the absolute id, use this to check if the pixel has been touched already
                abs_id = p_ops.get_pixel_by_row_col(tr_pixel[0], tr_pixel[1], self.width)

                if not self.pixel_list[abs_id].touched:
                    self.adj_pixels.append(abs_id)
                    discovered = True

        # Only check the left and right pixels if they exist (checks the edge of the image)
        if index % self.width != 0:
            #                       Row                            Column
            cl_pixel = [self.pixel_list[index].pix_row_id, self.pixel_list[index].pix_col_id - 1]

            # Find the absolute id, use this to check if the pixel has been touched already
            abs_id = p_ops.get_pixel_by_row_col(cl_pixel[0], cl_pixel[1], self.width)

            if not self.pixel_list[abs_id].touched:
                self.adj_pixels.append(abs_id)
                discovered = True

        if (index + 1) % self.width != 0:
            #                       Row                            Column
            cr_pixel = [self.pixel_list[index].pix_row_id, self.pixel_list[index].pix_col_id + 1]

            # Find the absolute id, use this to check if the pixel has been touched already
            abs_id = p_ops.get_pixel_by_row_col(cr_pixel[0], cr_pixel[1], self.width)

            if not self.pixel_list[abs_id].touched:
                self.adj_pixels.append(abs_id)
                discovered = True

        # Check the bottom pixels
        #                       Row                            Column
        bm_pixel = [self.pixel_list[index].pix_row_id + 1, self.pixel_list[index].pix_col_id]

        # Find the absolute id, use this to check if the pixel has been touched already
        abs_id = p_ops.get_pixel_by_row_col(bm_pixel[0], bm_pixel[1], self.width)

        if abs_id < (self.width * self.height):
            if not self.pixel_list[abs_id].touched:
                self.adj_pixels.append(abs_id)
                discovered = True

            if index % self.width != 0:
                #                   Row                            Column
                bl_pixel = [self.pixel_list[index].pix_row_id + 1, self.pixel_list[index].pix_col_id - 1]

                # Find the absolute id, use this to check if the pixel has been touched already
                abs_id = p_ops.get_pixel_by_row_col(bl_pixel[0], bl_pixel[1], self.width)

                if not self.pixel_list[abs_id].touched:
                    self.adj_pixels.append(abs_id)
                    discovered = True

            if index != (self.width * self.height - 1):
                #                   Row                            Column
                br_pixel = [self.pixel_list[index].pix_row_id + 1, self.pixel_list[index].pix_col_id + 1]

                # Find the absolute id, use this to check if the pixel has been touched already
                abs_id = p_ops.get_pixel_by_row_col(br_pixel[0], br_pixel[1], self.width)

                if not self.pixel_list[abs_id].touched:
                    self.adj_pixels.append(abs_id)
                    discovered = True

        return discovered

    def evaluate_connections(self):
        # Iterate through the found adjacent pixels and add them to storage to be processed
        for i in range(len(self.adj_pixels)):
            if self.pixel_list[self.adj_pixels[i]].all_colors == p_ops.all_white:
                self.pixel_list[self.adj_pixels[i]].touched = True

            elif not self.pixel_list[self.adj_pixels[i]].touched:
                self.pixel_list[self.adj_pixels[i]].touched = True
                self.storage_pixels.append(self.pixel_list[self.adj_pixels[i]])

        # Clean out the adjacent pixel list
        self.adj_pixels.clear()

        # Work on the first pixel in storage - pixels in storage have been touched and are used to continue searching
        # for additional neighboring pixels
        first_storage_pixel_abs_value = None

        if len(self.storage_pixels) != 0:
            self.found_pixels.append(self.storage_pixels[0])
            first_storage_pixel_abs_value = self.storage_pixels[0].global_id

        # Remove the pixel from storage
        self.storage_pixels = self.storage_pixels[1:]

        # Discover any connections to this pixel, if they are valid, add them to the storage list
        if first_storage_pixel_abs_value is not None:
            self.discover_connections(first_storage_pixel_abs_value)
            return True
        else:
            return False
