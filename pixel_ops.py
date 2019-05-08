#region ### Imports ###
import PIL.Image
#endregion

#region ### Globals ###
# The color white
white = 255
all_white = (255, 255, 255, 255)

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

        # The touched value, determines if the pixel has been check before
        # Default it is set to false
        self.touched = False

        # The hue of the pixel compared to all other pixels in an object, if its in an object
        self.hue = None

    def update_hue(self, hue):
        self.hue = hue


def get_orig_pixels(image):
    # Get the original pixel data from the image in list form
    return list(image.getdata())


def create_pixels(original_pixel_list, width):
    # Create a new list of pixels to return
    new_pixels = []

    for i in range(len(original_pixel_list)):
        red_value = original_pixel_list[i][0]    # Red RGB value from 0-255
        green_value = original_pixel_list[i][1]  # Green RGB value from 0-255
        blue_value = original_pixel_list[i][2]   # Blue RGB value from 0-255

        # Get the row and column of the pixel
        row, column = get_row_and_col(i, width)

        # Create and add the Pixel
        new_pixels.append(Pixel(i, row, column, red_value, green_value, blue_value))

    return new_pixels


def get_image_width_height(image):
    # Get the width and height of the image
    width, height = image.size

    return width, height


def get_row_and_col(pixel_index, width):
    # Get the quotient and the modulo
    row, col = divmod(pixel_index, width)

    return row, col


def get_pixel_gid_by_row_col(row, col, width):
    # Get the global id of the pixel from the row and column
    return (row * width) + col


def get_local_index_by_global_id(pixel_list, gid):
    # Iterate through the pixel list, and find the matching gid, return the local gid
    for i in range(len(pixel_list)):
        if pixel_list[i].global_id == gid:
            return i

    # Error
    return -1
