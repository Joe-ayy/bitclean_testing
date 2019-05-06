#region ### Imports ###
import PIL.Image
#endregion

# Globals for the color white
white = 255
all_white = (255, 255, 255, 255)


class Pixel:
    # Pixel ID, the relative location from the top left corner
    id = []

    # The RGB values of the pixel
    red = 0
    green = 0
    blue = 0

    # The touched value, determines if the pixel has been check before
    # Default it is set to false
    touched = False

    def __init__(self, row_id, col_id, r_value, g_value, b_value):
        self.id.append(row_id)
        self.id.append(col_id)
        self.red = r_value
        self.green = g_value
        self.blue = b_value


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
        temp_pixel = Pixel(row, column, red_value, green_value, blue_value)
        new_pixels.append(temp_pixel)

    return new_pixels


def get_width_height(image):
    # Get the width and height of the image
    width, height = image.size

    return width, height


def find_row_and_col(pixel_index, width):
    # Get the quotient and the modulo
    row, col = divmod(pixel_index, width)

    return row, col
