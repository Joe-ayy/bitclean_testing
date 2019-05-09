#region ### Imports ###
from copy import deepcopy
#endregion

#region ### Globals ###
# The color white
white = 255
all_white = (255, 255, 255, 255)

# The color black
black = 0
all_black = (0, 0, 0, 255)

# Set the alpha
alpha = 255
#endregion


class Pixel:
    def __init__(self, position, row_id, col_id, r_value, g_value, b_value):
        # Pixel global ID, in terms of top to bottom, right to left
        self.gid = position

        # Pixel ID, specified as row and column
        self.pixel_row_id = row_id
        self.pixel_col_id = col_id

        # The RGB values of the pixel
        self.red = r_value
        self.green = g_value
        self.blue = b_value

        # The RGB-A tuple of colors
        self.all_colors = (self.red, self.green, self.blue, alpha)

        # Set masks
        self.bbox_mask = [deepcopy(self.red), deepcopy(self.green), deepcopy(self.blue)]

        # The touched value, determines if the pixel has been check before
        # Default it is set to false
        self.touched = False

        # The hue of the pixel compared to all other pixels in an object, if its in an object
        self.hue = None

        # Set the RGB color to a corresponding int
        self.num_color = self.color_to_int()

    def update_hue(self, hue):
        self.hue = hue

    def color_to_int(self):
        # Code is converted from c# code written by Austin Herman located in imageops.cs in BitClean
        # Convert the pixel color from RGB to an int
        # Scales as (0, 0, 255) = 1 -> (255, 0, 0) = 1021

        # Check to see if the color is white
        if self.all_colors == all_white:
            num_color = 0
        elif self.all_colors == all_black:
            num_color = 0
        elif self.red == 255:
            num_color = self.red + (255 - self.green) + 510 + 1
        elif self.green == 255:
            num_color = self.red + self.green + 255 + 1
        else:
            num_color = self.green + 255 - self.blue + 1

        return num_color


def get_orig_pixels(image):
    # Get the original pixel data from the image in list form
    return list(image.getdata())


def create_pixel_matrix(orig_pixel_list, width, height):
    # Create a 2-D list (Matrix) containing all the pixels in the image
    pixel_matrix = [[None for _ in range(width)] for _ in range(height)]

    # Get the relevant pixel data and insert it to the matrix
    for i in range(height):
        for j in range(width):
            # Set the position index of the pixel
            pos_idx = i * width + j

            # Get the RGB values from the original pixel list
            red_value = orig_pixel_list[pos_idx][0]
            green_value = orig_pixel_list[pos_idx][1]
            blue_value = orig_pixel_list[pos_idx][2]

            # Get the row and the column of the pixel
            row = i
            column = j

            pixel_matrix[i][j] = Pixel(pos_idx, row, column, red_value, green_value, blue_value)

    # Return the created pixel matrix
    return pixel_matrix


def get_image_width_height(image):
    # Get the width and height of the image
    width, height = image.size

    return width, height


def get_row_and_col(pixel_index, width):
    # Get the quotient and the modulo
    row, col = divmod(pixel_index, width)

    return row, col


def get_gid_from_row_col(row, col, width):
    return (row * width) + col


def get_local_index_by_global_id(pixel_list, gid):
    # Iterate through the pixel list, and find the matching gid, return the local gid
    for i in range(len(pixel_list)):
        if pixel_list[i].global_id == gid:
            return i

    # Error
    return -1
