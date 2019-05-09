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

# Bubble sort algorithm mimicked from this site:
# https://www.w3resource.com/python-exercises/data-structures-and-algorithms/python-search-and-sorting-exercise-4.php


def sort_by_column(list_of_pixels):
    # Bubble sort
    for dummy in range(len(list_of_pixels) - 1, 0, -1):
        for i in range(dummy):
            if list_of_pixels[i].pixel_col_id > list_of_pixels[i + 1].pixel_col_id:
                temp = list_of_pixels[i]
                list_of_pixels[i] = list_of_pixels[i + 1]
                list_of_pixels[i + 1] = temp

    # Return
    return list_of_pixels
