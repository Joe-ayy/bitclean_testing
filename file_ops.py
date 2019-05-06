#region ### Imports ###
import PIL.Image
from tkinter.filedialog import *
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
