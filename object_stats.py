# region ### Imports ###
import pixel_ops as p_ops
#endregion


def get_avg_hue_object(store_object, return_format="single"):
    # Get the average RGB values
    avg_red = 0
    avg_green = 0
    avg_blue = 0

    # Number of pixels in object
    num_pixels = len(store_object.pixels_in_obj)

    for i in range(num_pixels):
        avg_red = avg_red + store_object.pixels_in_obj[i].red
        avg_green = avg_green + store_object.pixels_in_obj[i].green
        avg_blue = avg_blue + store_object.pixels_in_obj[i].blue

    avg_red = avg_red / num_pixels
    avg_green = avg_green / num_pixels
    avg_blue = avg_blue / num_pixels

    # Set the hues for the pixels
    for j in range(num_pixels):
        store_object.pixels_in_obj[j].update_hue((int(avg_red), int(avg_green), int(avg_blue)))

    # Return a tuple of all the averaged values
    if return_format == "tuple":
        ret_tuple = (int(avg_red), int(avg_green), int(avg_blue))
        return ret_tuple
    elif return_format == "single":
        # Find the average hue
        avg_hue = (avg_red + avg_green + avg_blue) / 3
        return avg_hue
    else:
        return -1


def get_avg_hue_of_row_or_col(list_of_pixels):
    # Get the average RGB values
    hue = 0

    # Get the number of pixels in the row or column
    num_pixels = len(list_of_pixels)

    # Add up the values of the colors
    for i in range(num_pixels):
        hue = hue + p_ops.color_to_int(list_of_pixels[i])

    # Get the average of the hue
    avg_hue = hue / num_pixels

    # Return the value
    return avg_hue


def get_size(store_object):  # Needs to utilize a filler to find the actual size of the object
    return len(store_object.pixels_in_obj)
