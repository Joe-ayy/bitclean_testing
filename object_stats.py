def get_avg_hue(store_object, return_format="single"):
    # Get the average RGB values
    avg_red = 0
    avg_green = 0
    avg_blue = 0

    # Number of pixels in object
    num_pixels = len(store_object.selection)

    for i in range(num_pixels):
        avg_red = avg_red + store_object.selection[i].red
        avg_green = avg_green + store_object.selection[i].green
        avg_blue = avg_blue + store_object.selection[i].blue

    avg_red = avg_red / num_pixels
    avg_green = avg_green / num_pixels
    avg_blue = avg_blue / num_pixels

    # Set the hues for the pixels
    for j in range(num_pixels):
        store_object.selection[j].update_hue((int(avg_red), int(avg_green), int(avg_blue)))

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


def get_size(store_object):  # Needs to utilize a filler to find the actual size of the object
    return len(store_object.selection)
