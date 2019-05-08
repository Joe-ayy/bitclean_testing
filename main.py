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
    img_width, img_height = p_ops.get_image_width_height(img)

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
    print("Store objects found")

    # Set the average hue of pixels in store objects
    for i in range(len(store_map.objects_in_store)):
        o_stats.get_avg_hue(store_map.objects_in_store[i], "toss")  # Toss input doesn't matter

    data_processing_stop = time.time()
    data_processing_elapsed_time = data_processing_stop - start

    print("Elapsed time for data processing: ", datetime.timedelta(seconds=data_processing_elapsed_time))

    # Testing, save the image
    f_ops.create_and_save_bw_image(pixels, img_width, img_height)

    # Printing
    print("Store map created in black and white")

    # Testing, save the image
    f_ops.create_and_save_avg_hue_image(pixels, img_width, img_height)

    # Printing
    print("Store map created with average hue per object")

    # Create bounding boxes and save to image
    store_map.transform_bbox_pixels()
    f_ops.create_and_save_bbox_image(store_map)

    # Printing
    print("Store map created with bounding boxes")

    # Printing
    store_map.print_all_objects_width_and_height_to_console()

    stop = time.time()
    elapsed_time = stop - start

    print("Total elapsed time: ", datetime.timedelta(seconds=elapsed_time))


main()
