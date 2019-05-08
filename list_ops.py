# region ### Imports
#endregion


# Mimic the insort function found from bisect module
# Referenced code:
# https://stackoverflow.com/questions/41902958/insert-item-into-case-insensitive-sorted-list-in-python/41903429#41903429


def insort_pixels(list_of_pixels, pxl):
    # Generate a key from the pixel
    key = pxl.gid

    # Specify the low and high points
    low, high = 0, len(list_of_pixels)

    # Perform binary search
    while low < high:
        mid_pt = (low + high) // 2
        if key < list_of_pixels[mid_pt].gid:
            high = mid_pt
        else:
            low = mid_pt + 1

    list_of_pixels.insert(low, pxl)
