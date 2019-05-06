#region ### Imports ###
import PIL.Image
import file_ops as f_ops
import pixel_ops as p_ops
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


main()
