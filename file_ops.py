#region ### Imports ###
import PIL.Image
from tkinter.filedialog import *
import pixel_ops as p_ops
import object_stats as o_stats
#endregion


def load_and_create_image():
    # Ask the user for a filename and return an image object

    # Using TK, ask for the file name
    Tk().withdraw()
    bmp_name = askopenfilename(filetypes=(("bmp files", "*.bmp"), ("all files", "*.*")))

    # Create an image object and open the image in it
    bmp_img = PIL.Image.open(bmp_name)

    # Return the created image
    return bmp_img


def create_and_save_bw_image(list_of_pixels, w, h):
    # Initialize a list of pixels to send to a file
    file_pixels = []

    for i in range(len(list_of_pixels)):
        if list_of_pixels[i].all_colors != p_ops.all_white:
            file_pixels.append((0, 0, 0))
        else:
            file_pixels.append((255, 255, 255))

    save_img = PIL.Image.new("RGB", (w, h))
    save_img.putdata(file_pixels)
    save_img.save("bw_output.bmp")


def create_and_save_avg_hue_image(list_of_pixels, w, h):
    # Initialize a list of pixels to send to a file
    file_pixels = []

    for i in range(len(list_of_pixels)):
        if list_of_pixels[i].hue is not None:
            file_pixels.append(list_of_pixels[i].hue)
        else:
            file_pixels.append((255, 255, 255))

    save_img = PIL.Image.new("RGB", (w, h))
    save_img.putdata(file_pixels)
    save_img.save("avg_hue_output.bmp")
