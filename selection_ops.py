#region ### Imports ###
import tree_ops as t_ops
import pixel_ops as p_ops
#endregion


class StoreObject:
    # The objects in this class are objects found in a store map, they will either be determined to be a structure or
    # dust (something not actually present in the store)

    object_type = None  # This will either be set to "structure" or "dust"

    def __init__(self, data):
        # Create a binary tree to hold all the pixels that belong to this StoreObject
        self.selection = t_ops.BinaryTreeNode(data)


class StoreMap:
    # Temporarily store a list of all pixels found per object
    found_pixels = []

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

                    # Find and add all the connections of this object to this instance of StoreObject
                    self.discover_connections(i, [])

                    for j in range(len(self.found_pixels)):
                        object_in_store.selection.insert_node(self.found_pixels[j])

                    # Empty the temporary found_pixels list
                    self.found_pixels.clear()

                    # Add this object to the store_objects list
                    store_objects.append(object_in_store)

        return store_objects

    def discover_connections(self, index, pixels_2_check):
        # Initialize a list to hold all the adjacent pixels
        adj_pixels = []
        adj_pixels.extend(pixels_2_check)

        # Find all the neighboring pixels to the originally found pixel and add them to the tree

        # Find any adjacent pixels that are non-white using this diagram
        # TL TM TR - Top Left, Top Middle, Top Right
        # CL XX CR - Center Left, XX is Current Pixel, Center Right
        # BL BM BR - Bottom Left, Bottom Middle, Bottom Right

        # Only check the top pixels if a row above the current one exists
        if index > self.width:
            #                       Row                            Column
            tm_pixel = [self.pixel_list[index].pix_row_id - 1, self.pixel_list[index].pix_col_id]
            adj_pixels.append(tm_pixel)

            if index % self.width != 0:
                #                       Row                            Column
                tl_pixel = [self.pixel_list[index].pix_row_id - 1, self.pixel_list[index].pix_col_id - 1]
                adj_pixels.append(tl_pixel)

            if (index + 1) % self.width != 0:
                #                       Row                            Column
                tr_pixel = [self.pixel_list[index].pix_row_id - 1, self.pixel_list[index].pix_col_id + 1]
                adj_pixels.append(tr_pixel)

        # Only check the left and right pixels if they exist (checks the edge of the image)
        if index % self.width != 0:
            #                       Row                            Column
            cl_pixel = [self.pixel_list[index].pix_row_id, self.pixel_list[index].pix_col_id - 1]
            adj_pixels.append(cl_pixel)

        if (index + 1) % self.width != 0:
            #                       Row                            Column
            cr_pixel = [self.pixel_list[index].pix_row_id, self.pixel_list[index].pix_col_id + 1]
            adj_pixels.append(cr_pixel)

        # Only check the bottom pixels if a row below the current one exists
        if index < (self.width * self.height):
            #                       Row                            Column
            bm_pixel = [self.pixel_list[index].pix_row_id + 1, self.pixel_list[index].pix_col_id]
            adj_pixels.append(bm_pixel)

            if index % self.width != 0:
                #                   Row                            Column
                bl_pixel = [self.pixel_list[index].pix_row_id + 1, self.pixel_list[index].pix_col_id - 1]
                adj_pixels.append(bl_pixel)

            if index != self.width * self.height:
                #                   Row                            Column
                br_pixel = [self.pixel_list[index].pix_row_id + 1, self.pixel_list[index].pix_col_id + 1]
                adj_pixels.append(br_pixel)

        for i in range(len(adj_pixels)):
            # Get the global id of the pixel
            absolute_id = p_ops.get_pixel_by_row_col(adj_pixels[i][0], adj_pixels[i][1], self.width)

            # Check if this pixel has not been touched
            if not self.pixel_list[absolute_id].touched:
                # Check to see if this pixel is non-white
                if self.pixel_list[absolute_id].all_colors != p_ops.all_white:
                    # Add this pixel to the StoreObject tree and call this function on that pixel, this should
                    # find all the connections for this object, save all the pixel values, and set the touched value to
                    # true
                    self.found_pixels.append(absolute_id)
                    self.pixel_list[absolute_id].touched = True
                    self.discover_connections(absolute_id, adj_pixels[i+1:])
