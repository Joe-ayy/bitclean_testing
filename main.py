# Code derived from BitClean, a C# program developed by Austin Herman
# Github link: https://github.com/austeeen/bitclean

#region ### Imports ###
import PIL.Image
import file_ops as f_ops
import pixel_ops as p_ops
import selection_ops as s_ops
import object_stats as o_stats
import time
import datetime
#endregion


def main():
    start = time.time()

    # Get an image object from a file
    img = f_ops.load_and_create_image()

    # Printing
    print("Image loaded")

    # Get the width and height of the image
    img_width, img_height = p_ops.get_width_height(img)

    # Printing
    print("Image width and height received")

    # Get all the pixel values of the image
    orig_pixels = p_ops.get_orig_pixels(img)

    # Printing
    print("Original pixel values received")

    # Create a list of pixels defined by the Pixel Class
    pixels = p_ops.create_pixels(orig_pixels, img_width)

    # Printing
    print("New pixel values calculated")

    # Create an instance of StoreMap to find all the objects in the store
    store_map = s_ops.StoreMap(pixels, img_width, img_height)

    # Printing
    print("Store map created")

    list_of_store_objects = store_map.find_objects_in_store()

    # Set the average hue of pixels in store objects
    for i in range(len(list_of_store_objects)):
        o_stats.get_avg_hue(list_of_store_objects[i], "toss")

    # Printing
    print("Store objects found")

    # Testing, save the image
    f_ops.create_and_save_bw_image(pixels, img_width, img_height)

    # Printing
    print("Store map created in black and white")

    # Testing, save the image
    f_ops.create_and_save_avg_hue_image(pixels, img_width, img_height)

    # Printing
    print("Store map created with average hue per object")

    stop = time.time()

    elapsed_time = stop - start

    print("Elapsed time: ", datetime.timedelta(seconds=elapsed_time))


main()
