#region ### Imports ###
import PIL.Image
from tkinter.filedialog import *
import pixel_ops as p_ops
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


def create_and_save_bw_image(store):
    # Initialize a list of pixels to send to a file
    file_pixels = []

    for i in range(len(store.pixel_matrix)):
        for j in range(len(store.pixel_matrix[0])):
            if store.pixel_matrix[i][j].all_colors != p_ops.all_white:
                file_pixels.append((0, 0, 0))
            else:
                file_pixels.append((255, 255, 255))

    save_img = PIL.Image.new("RGB", (store.img_width, store.img_height))
    save_img.putdata(file_pixels)
    save_img.save("bw_output.bmp")


def create_and_save_avg_hue_image(store):
    # Initialize a list of pixels to send to a file
    file_pixels = []

    for i in range(len(store.pixel_matrix)):
        for j in range(len(store.pixel_matrix[0])):
            if store.pixel_matrix[i][j].hue is not None:
                file_pixels.append(store.pixel_matrix[i][j].hue)
            else:
                file_pixels.append((255, 255, 255))

    save_img = PIL.Image.new("RGB", (store.img_width, store.img_height))
    save_img.putdata(file_pixels)
    save_img.save("avg_hue_output.bmp")


def create_and_save_bbox_image(store):
    # Initialize a list of pixels to send to a file
    file_pixels = []

    for i in range(len(store.pixel_matrix)):
        for j in range(len(store.pixel_matrix[0])):
            file_pixels.append(tuple(store.pixel_matrix[i][j].bbox_mask))

    save_img = PIL.Image.new("RGB", (store.img_width, store.img_height))
    save_img.putdata(file_pixels)
    save_img.save("bounding_box_output.bmp")
