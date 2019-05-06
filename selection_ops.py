class StoreObject:
    # The objects in this class are objects found in a store map, they will either be determined to be a structure or
    # dust (something not actually present in the store)

    object_type = None  # This will either be set to "structure" or "dust"


def find_objects_in_store(pixel_list):
    # Iterate through the list of pixels to find objects in the store
    # These objects will be the non-white pixels connected to 0 or more non-white pixels and are to be determined
    # in the future to be either a structure present in the store or dust
    