# region ### Imports
#endregion


# Mimic the insort function found from bisect module
# Referenced code:
# https://stackoverflow.com/questions/41902958/insert-item-into-case-insensitive-sorted-list-in-python/41903429#41903429


def insort_pixels(p_list, pxl):
    # Generate a key from the pixel
    key = pxl.global_id

    # Specify the low and high points
    low, high = 0, len(p_list)

    # Perform binary search
    while low < high:
        mid_pt = (low + high) // 2
        if key < p_list[mid_pt].global_id:
            high = mid_pt
        else:
            low = mid_pt + 1

    p_list.insert(low, pxl)
