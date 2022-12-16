"""
CSE331 Project 5 FS'22
Circular Double-Ended Queue
solution.py
"""
from typing import TypeVar, List
from random import randint, shuffle
from timeit import default_timer
#from matplotlib import pyplot as plt  # COMMENT OUT THIS LINE (and `plot_speed`) if you dont want matplotlib
import gc

T = TypeVar('T')


class CircularDeque:
    """
    Representation of a Circular Deque using an underlying python list
    """

    __slots__ = ['capacity', 'size', 'queue', 'front', 'back']

    def __init__(self, data: List[T] = None, front: int = 0, capacity: int = 4):
        """
        Initializes an instance of a CircularDeque
        :param data: starting data to add to the deque, for testing purposes
        :param front: where to begin the insertions, for testing purposes
        :param capacity: number of slots in the Deque
        """
        if data is None and front != 0:
            data = ['Start']  # front will get set to 0 by a front enqueue if the initial data is empty
        elif data is None:
            data = []

        self.capacity: int = capacity
        self.size: int = len(data)
        self.queue: List[T] = [None] * capacity
        self.back: int = (self.size + front - 1) % self.capacity if data else None
        self.front: int = front if data else None

        for index, value in enumerate(data):
            self.queue[(index + front) % capacity] = value

    def __str__(self) -> str:
        """
        Provides a string representation of a CircularDeque
        'F' indicates front value
        'B' indicates back value
        :return: the instance as a string
        """
        if self.size == 0:
            return "CircularDeque <empty>"

        str_list = ["CircularDeque <"]
        for i in range(self.capacity):
            str_list.append(f"{self.queue[i]}")
            if i == self.front:
                str_list.append('(F)')
            elif i == self.back:
                str_list.append('(B)')
            if i < self.capacity - 1:
                str_list.append(',')

        str_list.append(">")
        return "".join(str_list)

    __repr__ = __str__

    #
    # Your code goes here!
    #
    def __len__(self) -> int:
        """
        Returns the length/size of the circular deque
        :return: int representing length of the circular deque
        """
        return self.size

    def is_empty(self) -> bool:
        """
        Returns a boolean indicating if the circular deque is empty
        :return: bool True if empty, False otherwise
        """
        if self.size == 0:
            return True
        else:
            return False

    def front_element(self) -> T:
        """
        Returns the first element in the circular deque
        :return: The first element if it exists, otherwise None
        """
        if self.front == None:
            return None
        return self.queue[self.front]

    def back_element(self) -> T:
        """
        Returns the last element in the circular deque
        :return: The last element if it exists, otherwise None
        """
        if self.back is None:
            return None
        return self.queue[self.back]


    def enqueue(self, value: T, front: bool = True) -> None:
        """
        Add a value to either the front or back of the circular deque based off the parameter front
        :param value: value to add into the circular deque
        :param front: boolean indicating where to add value into the deque. If true add to front, otherwise add to back
        :return: None
        """

        if front == True:   # enqueue to front
            # check if CD is empty
            if self.is_empty() == True:
                self.front = 0
                self.back = 0
                self.queue[self.front] = value
            else:
                self.front = (self.front - 1) % self.capacity
                self.queue[self.front] = value

        elif front != True:   # enqueue to back
            # check if CD is empty
            if self.is_empty() == True:
                self.front = 0
                self.back = 0
                self.queue[self.back] = value
            else:
                self.back = (self.back + 1) % self.capacity
                self.queue[self.back] = value

        self.size += 1
        if self.size == self.capacity:
            self.grow()

    def dequeue(self, front: bool = True) -> T:
        """
        Removes the front item from CD by default, remove the back item if False is passed in
        :param front: Whether to remove the front or back item from the dequeue
        :return removed item, None if empty
        """
        # check if CD is empty
        if self.is_empty() == True:
            return None
        if front == True:   # dequeue from front
            removed_item = self.queue[self.front]
            self.front = (self.front + 1) % self.capacity
            self.size -= 1

        elif front != True:    # dequeue from back
            removed_item = self.queue[self.back]
            self.back = (self.back - 1) % self.capacity
            self.size -= 1

        # shrink CD if necessary
        if self.size <= (self.capacity / 4):
            self.shrink()
        return removed_item

    def grow(self) -> None:
        """
        Doubles the capacity of CD by creating a new underlying python list with double
        the capacity of the old one and copies the values over from the current list
        :return None
        """

        if self.is_empty():
            new_list = [None] * (self.capacity * 2)
        else:
            new_list = [None] * (self.size * 2)

            # copy values from original CD to new_list
            for i in range(0, self.capacity):
                if i >= self.front:
                    new_list[i - self.front] = self.queue[i]
                elif i < self.front:
                    new_list[(i + self.capacity) - self.front] = self.queue[i]

        self.queue = new_list
        self.capacity = self.capacity * 2
        self.front = 0
        self.back = self.size-1



    def shrink(self) -> None:
        """
        Cuts the capacity of the queue in half using the same idea as grow.
        Copy over contents of the old list to a new list with half the capacity
        :return None
        """

        empty_spots = self.capacity - self.size
        # new size
        if (self.capacity / 2) < 4:
            return
        self.capacity = self.capacity // 2

        # create list of non-empty vals from initial list
        original_vals = []
        for i in range(self.front, self.back+1):
            original_vals.append(self.queue[i])

        new_list = original_vals + ([None] * (abs(self.capacity - empty_spots)))

        self.queue = new_list
        self.front = 0
        self.back = self.size - 1

class File:
    """
    File class stores data, used in application problem
    """
    def __init__(self, data : str) -> None:
        """
        Creates a file with data value
        :param : data , data to be stored in file
        :returns : None
        """
        self.data = data

    def __eq__(self, other: 'File') -> bool:
        """
        Compares two Files by data
        :param other: the other file
        :return: true if comparison is true, else false
        """
        return self.data == other.data

    def __str__(self) -> str:
        """
        :return: a string representation of the File
        """
        return f'File: {self.data}'

    __repr__ = __str__

def filter_corrupted(directory : List[File]) -> int:
    """
    Uncorrupt the data by finding the largest list of files without any repeats
    :param directory: List[File]: directory list of files to be looked through
    :return: integer representing the size of the largest list of files without repeats
    """

    # Initial solution. Works but doesn't pass edge cases.
    # Also doesn't really utilize CD functionality
    """
    if len(directory) == 0:
        return 0
    cd = CircularDeque()
    unique_vals = set()
    max_count = 0
    for file in directory:
        cd.enqueue(file)
        unique_vals.add(file.data)
        if cd.size > len(unique_vals):    # dupe found
            if len(unique_vals) > max_count:  # update max if necessary
                max_count = len(unique_vals)
            unique_vals.clear()      # reset unique_vals for next series of files
            cd.size = 0
    if len(unique_vals) > max_count:
        max_count = len(unique_vals)
    return max_count
    """

    # Second solution. Works for edge cases and takes advantage of CD functionality
    if len(directory) == 0:
        return 0
    cd = CircularDeque()
    unique_vals = dict()
    max_count = 0
    for file in directory:
        cd.enqueue(file, front=False)
        if file.data not in unique_vals:
            unique_vals[file.data] = 1
        elif file.data in unique_vals:
            unique_vals[file.data] += 1
        if cd.size > len(unique_vals):    # dupe found
            if len(unique_vals) > max_count:  # update max if necessary
                max_count = len(unique_vals)
            first_file = cd.dequeue()
            if unique_vals[first_file.data] > 1:
                unique_vals[first_file.data] -= 1
            else:
                del unique_vals[first_file.data]
        elif len(unique_vals) > max_count:
            max_count = len(unique_vals)
    if len(unique_vals) > max_count:
        max_count = len(unique_vals)
    return max_count





