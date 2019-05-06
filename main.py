# Code derived from BitClean, a C# program developed by Austin Herman
# Github link: https://github.com/austeeen/bitclean

#region ### Imports ###
import PIL.Image
import file_ops as f_ops
import pixel_ops as p_ops
import selection_ops as s_ops
#endregion


def main():
    # Get an image object from a file
    img = f_ops.load_and_create_image()

    # Get the width and height of the image
    img_width, img_height = p_ops.get_width_height(img)

    # Get all the pixel values of the image
    orig_pixels = p_ops.get_orig_pixels(img)

    # Create a list of pixels defined by the Pixel Class
    pixels = p_ops.create_pixels(orig_pixels, img_width)

    # Create an instance of StoreMap to find all the objects in the store
    store_map = s_ops.StoreMap(pixels, img_width, img_height)

    list_of_store_objects = store_map.find_objects_in_store()

    print(1001)


main()
