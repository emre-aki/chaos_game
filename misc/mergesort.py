def mergesort(array):
    """
    Sorts given list of elements
    :param array: list of elements to be sorted
    :return: sorted list of elements
    """
    if len(array) == 1:
        return array
    else:
        size_half = len(array) // 2
        left_subarray = mergesort(array[:size_half])
        right_subarray = mergesort(array[size_half:])
        merged_array = []
        i = 0
        j = 0
        while i < len(left_subarray) and j < len(right_subarray):
            if left_subarray[i] <= right_subarray[j] :
                merged_array.append(left_subarray[i])
                i += 1
            else:
                merged_array.append(right_subarray[j])
                j += 1
        while i < len(left_subarray):
            merged_array.append(left_subarray[i])
            i += 1
        while j < len(right_subarray):
            merged_array.append(right_subarray[j])
            j += 1
        return merged_array