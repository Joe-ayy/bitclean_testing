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
    # Pixel ID, in terms of top to bottom, right to left
    global_id = None

    # Pixel ID, specified as row, column pair
    pix_row_id = None
    pix_col_id = None

    # The RGB values of the pixel
    red = 0
    green = 0
    blue = 0

    # The touched value, determines if the pixel has been check before
    # Default it is set to false
    touched = False

    def __init__(self, position, row_id, col_id, r_value, g_value, b_value):
        self.global_id = position
        self.pix_row_id = row_id
        self.pix_col_id = col_id
        self.red = r_value
        self.green = g_value
        self.blue = b_value
        self.all_colors = (self.red, self.green, self.blue, alpha)


def get_orig_pixels(image):
    # Get the original pixel data from the image in list form
    return list(image.getdata())


def create_pixels(orig_pixels, width):
    # Create a new list of pixels to return
    new_pixels = []

    for i in range(len(orig_pixels)):
        red_value = orig_pixels[i][0]    # Red RGB value from 0-255
        green_value = orig_pixels[i][1]  # Green RGB value from 0-255
        blue_value = orig_pixels[i][2]   # Blue RGB value from 0-255

        # Get the row and column of the pixel
        row, column = find_row_and_col(i, width)

        # Create and add the Pixel
        new_pixels.append(Pixel(i, row, column, red_value, green_value, blue_value))

    return new_pixels


def get_width_height(image):
    # Get the width and height of the image
    width, height = image.size

    return width, height


def find_row_and_col(pixel_index, width):
    # Get the quotient and the modulo
    row, col = divmod(pixel_index, width)

    return row, col


def get_pixel_by_row_col(row, col, width):
    # Get the global id of the pixel from the row and column
    return (row * width) + col
