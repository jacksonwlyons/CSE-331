"""
Project 4 - Hybrid Sorting - Solution Code
CSE 331 Fall 2022
"""

import gc
import random
import time
from typing import TypeVar, List, Callable, Dict

T = TypeVar("T")  # represents generic type


# do_comparison is an optional helper function but HIGHLY recommended!!!
def do_comparison(first: T, second: T, key: Callable[[T], T], descending: bool) -> bool:
    """
    Tells you whether to put `first` before `second` in the sorted list
    :param first: first element to be compared
    :param second: second element to be compared
    :param key: custom argument which returns a certain function done on the data in the list
    :param descending: boolean indicating whether to compare first and second in descending order
    :return bool indicating whether to put first before second. Function will return true
    if first should be before second and false otherwise
    """
    if descending != True:
        if key(first) < key(second):
            return True
        else:
            return False
    else:   # descending is true
        if key(first) > key(second):
            return True
        else:
            return False


def selection_sort(data: List[T], *, key: Callable[[T], T] = lambda x: x,
                   descending: bool = False) -> None:
    """
    This function will sort a list of values in-place using the selection sort algorithm
    :param data: List of items to be sorted
    :param key: A function which takes an argument of type T and returns new value of first argument
    :param descending: Perform the sort in descending order when this is True. Defaults to False
    :return None
    """
    for i in range(len(data) - 1):
        min_index = i
        for j in range(i + 1, len(data)):
            order_bool = do_comparison(data[j], data[min_index], key, descending)
            if order_bool == True:
                min_index = j

        data[i], data[min_index] = data[min_index], data[i]


def bubble_sort(data: List[T], *, key: Callable[[T], T] = lambda x: x,
                descending: bool = False) -> None:
    """
    This function will sort a list of values in-place using the bubble sort algorithm
    :param data: List of items to be sorted
    :param key: A function which takes an argument of type T and returns new value of first argument
    :param descending: Perform the sort in descending order when this is True. Defaults to False
    :return None
    """
    for i in range(len(data)):
        for j in range(len(data)-1):
            order_bool = do_comparison(data[j+1], data[j], key, descending)
            if order_bool == True:
                data[j], data[j+1] = data[j+1], data[j]


def insertion_sort(data: List[T], *, key: Callable[[T], T] = lambda x: x,
                   descending: bool = False) -> None:
    """
    Given a list of values this function will sort that list in-place using the insertion sort algorithm
    :param data: List of items to be sorted
    :param key: A function which takes an argument of type T and returns new value of first argument
    :param descending: Perform the sort in descending order when this is True. Defaults to False
    return: None
    """
    for i in range(1, len(data)):
        j = i
        while j > 0 and (do_comparison(data[j], data[j-1], key, descending) == True):
            data[j], data[j-1] = data[j-1], data[j]
            j = j - 1


# This function was partly inspired from https://favtutor.com/blogs/merge-sort-python
def h_merge_sort(data, key, descending, threshold):
    """
    Helper function for hybrid_merge_sort()
    Given a list of values, this function will sort that list using a
    hybrid sort with the merge sort and insertion sort algorithms
    :param data: List of items to be sorted
    :param key: A function which takes an argument of type T and returns new value of first argument
    :param descending: Perform the sort in descending order when this is True. Defaults to False
    :param threshold: Maximum size at which insertion sort will be used instead of merge sort
    :return: None
    """
    length = len(data)
    if length > 1:
        # if length is less than or equal to threshold, perform insertion sort
        if length <= threshold:
            insertion_sort(data, key=key, descending=descending)
        # otherwise continue doing merge sort
        else:
            mid = len(data)//2
            left = data[:mid]
            right = data[mid:]

            # Sort the two halves recursively
            h_merge_sort(left, key, descending, threshold)
            h_merge_sort(right, key, descending, threshold)
            i = j = k = 0

            while i < len(left) and j < len(right):
                if descending == False:   # sort ascending
                    if key(left[i]) < key(right[j]):
                        data[k] = left[i]
                        i += 1
                    else:
                        data[k] = right[j]
                        j += 1
                    k += 1
                else:    # sort descending
                    if key(left[i]) > key(right[j]):
                        data[k] = left[i]
                        i += 1
                    else:
                        data[k] = right[j]
                        j += 1
                    k += 1

            while i < len(left):
                data[k] = left[i]
                i += 1
                k += 1

            while j < len(right):
                data[k] = right[j]
                j += 1
                k += 1


def hybrid_merge_sort(data: List[T], *, threshold: int = 12,
                      key: Callable[[T], T] = lambda x: x, descending: bool = False) -> None:
    """
    Given a list of values, this function will sort that list using a
    hybrid sort with the merge sort and insertion sort algorithms
    :param data: List of items to be sorted
    :param threshold: Maximum size at which insertion sort will be used instead of merge sort
    :param key: A function which takes an argument of type T and returns new value of first argument
    :param descending: Perform the sort in descending order when this is True. Defaults to False
    return: None
    """
    if len(data) <= threshold:  # if size of data is smaller than threshold, perform insertion sort
        insertion_sort(data, key=key, descending=descending)
    else:   # otherwise perform merge sort
        h_merge_sort(data, key, descending, threshold)


# A hybrid quicksort would be even faster, but we don't want to give too much code away here!
def quicksort(data):
    """
    Sorts a list in place using quicksort
    :param data: Data to sort
    """

    def quicksort_inner(first, last):
        """
        Sorts portion of list at indices in interval [first, last] using quicksort

        :param first: first index of portion of data to sort
        :param last: last index of portion of data to sort
        """
        # List must already be sorted in this case
        if first >= last:
            return

        left = first
        right = last

        # Need to start by getting median of 3 to use for pivot
        # We can do this by sorting the first, middle, and last elements
        midpoint = (right - left) // 2 + left
        if data[left] > data[right]:
            data[left], data[right] = data[right], data[left]
        if data[left] > data[midpoint]:
            data[left], data[midpoint] = data[midpoint], data[left]
        if data[midpoint] > data[right]:
            data[midpoint], data[right] = data[right], data[midpoint]
        # data[midpoint] now contains the median of first, last, and middle elements
        pivot = data[midpoint]
        # First and last elements are already on right side of pivot since they are sorted
        left += 1
        right -= 1

        # Move pointers until they cross
        while left <= right:
            # Move left and right pointers until they cross or reach values which could be swapped
            # Anything < pivot must move to left side, anything > pivot must move to right side
            #
            # Not allowing one pointer to stop moving when it reached the pivot (data[left/right] == pivot)
            # could cause one pointer to move all the way to one side in the pathological case of the pivot being
            # the min or max element, leading to infinitely calling the inner function on the same indices without
            # ever swapping
            while left <= right and data[left] < pivot:
                left += 1
            while left <= right and data[right] > pivot:
                right -= 1

            # Swap, but only if pointers haven't crossed
            if left <= right:
                data[left], data[right] = data[right], data[left]
                left += 1
                right -= 1

        quicksort_inner(first, left - 1)
        quicksort_inner(left, last)

    # Perform sort in the inner function
    quicksort_inner(0, len(data) - 1)


def sort_sushi(sushi: List[str], key: Callable[[T], T] = lambda x: {'D': 0, 'A': 1, 'C': 2}[x]) -> None:
    """
    Sorts the list of sushi rolls in-place such that all the sushi rolls
    of the same type are together and that the sushi types appear in the
    order specified by the key dictionary
    :param sushi: The list of sushi string characters to sort
    :param key: The function that specifies the order in which the sushi rolls will be sorted
    :return None
    """
    # First solution - Doesn't sort list in one pass.
    """
    # Move first letters to front
    first_letter_index = 0
    for i in range(len(sushi)):
        if key(sushi[i]) == 0:
            sushi[first_letter_index], sushi[i] = sushi[i], sushi[first_letter_index]
            first_letter_index += 1
    # Move second letters after first
    for i in range(first_letter_index, len(sushi)):
        if key(sushi[i]) == 1:
            sushi[first_letter_index], sushi[i] = sushi[i], sushi[first_letter_index]
            first_letter_index += 1
    # Last letters should be at end.
    """
    # Second solution - Not as simple but sorts in one pass.
    #
    # initialize indexes to keep track of positions for swaps.
    first_letter_index = 0
    second_letter_index = 0
    if len(sushi) > 1:
        # If the first letter in list is in correct position increment indexes for next swap.
        if key(sushi[0]) == 0:
            first_letter_index += 1
            second_letter_index += 1
        for i in range(1, len(sushi)):
            # check if letter should be first
            if key(sushi[i]) == 0:
                # perform necessary swaps and increment first and second letter indexes
                if key(sushi[first_letter_index]) == 1 and key(sushi[first_letter_index+1]) == 1:
                    # since there is two or more second priority letters in a row. Only increment first_letter_index
                    sushi[first_letter_index], sushi[i] = sushi[i], sushi[first_letter_index]
                    first_letter_index += 1
                else:
                    sushi[first_letter_index], sushi[i] = sushi[i], sushi[first_letter_index]
                    first_letter_index += 1
                    second_letter_index += 1
            # check if letter should be second
            if key(sushi[i]) == 1:
                # perform necessary swaps and increment first and second letter indexes
                if key(sushi[first_letter_index]) != 1:
                    sushi[first_letter_index], sushi[i] = sushi[i], sushi[first_letter_index]
                    second_letter_index = first_letter_index + 1
                else:
                    if key(sushi[second_letter_index]) == 1 and (second_letter_index + 1 < len(sushi) - 1):
                        # avoid swapping letters of same priority by incrementing
                        second_letter_index += 1
                    if i >= second_letter_index:
                        # avoid swapping letters past index i
                        sushi[second_letter_index], sushi[i] = sushi[i], sushi[second_letter_index]
                        second_letter_index += 1
            # After sorting for first and second letter. The third letter should naturally be in its place at end of list

