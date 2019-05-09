# Code derived from BitClean, a C# program developed by Austin Herman
# Github link: https://github.com/austeeen/bitclean

#region ### Imports ###
import file_ops as f_ops
import pixel_ops as p_ops
import selection_ops as s_ops
import time
import datetime
#endregion


def main():
    # Start timer
    start = time.time()
    print("Program started")

    # Get an image object from a file
    img = f_ops.load_and_create_image()
    # Get the width and height of the image
    img_width, img_height = p_ops.get_image_width_height(img)
    # Get all the pixel values of the image
    orig_pixels = p_ops.get_orig_pixels(img)

    # Create a list of pixels defined by the Pixel Class
    new_pixels = p_ops.create_pixel_matrix(orig_pixels, img_width, img_height)
    print("New pixel values calculated in matrix form")

    # Create a store map to hold all the information about the store
    store_map = s_ops.StoreMap(new_pixels, img_width, img_height)

    data_processing_stop = time.time()
    data_processing_elapsed_time = data_processing_stop - start
    print("Elapsed time for data processing: ", datetime.timedelta(seconds=data_processing_elapsed_time))

    # Create and save images
    f_ops.create_and_save_bw_image(store_map)
    f_ops.create_and_save_bbox_image(store_map)
    store_map.set_hues_for_file_output()
    f_ops.create_and_save_avg_hue_image(store_map)
    print("Images created and saved")

    stop = time.time()
    elapsed_time = stop - start
    print("Total elapsed time: ", datetime.timedelta(seconds=elapsed_time))


main()
