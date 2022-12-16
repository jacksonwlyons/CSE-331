"""
Project 8 - Heaps - Solution Code
CSE 331 Fall2022
Onsay
Jackson Lyons
"""

from typing import TypeVar, List

T = TypeVar('T')


class MinHeap:
    """
    Partially completed data structure. Do not modify completed portions in any way
    """
    __slots__ = ['data']

    def __init__(self):
        """
        Initializes the priority heap
        """
        self.data = []

    def __str__(self) -> str:
        """
        Converts the priority heap to a string
        :return: string representation of the heap
        """
        return ', '.join(str(item) for item in self.data)

    __repr__ = __str__

    def to_tree_format_string(self) -> str:
        """
        Prints heap in Breadth First Ordering Format
        :return: String to print
        """
        string = ""
        # level spacing - init
        nodes_on_level = 0
        level_limit = 1
        spaces = 10 * int(1 + len(self))

        for i in range(len(self)):
            space = spaces // level_limit
            # determine spacing

            # add node to str and add spacing
            string += str(self.data[i]).center(space, ' ')

            # check if moving to next level
            nodes_on_level += 1
            if nodes_on_level == level_limit:
                string += '\n'
                level_limit *= 2
                nodes_on_level = 0
            i += 1

        return string

    #   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #   Modify below this line

    def __len__(self) -> int:
        """
        Returns the length of the heap
        :return: int representing length of heap
        """
        return len(self.data)

    def empty(self) -> bool:
        """
        Checks if the heap is empty
        :return: boolean stating if the heap is empty or not
        """
        if len(self) == 0:
            return True
        return False

    def top(self) -> T:
        """
        Returns the top value of the MinHeap
        :return: top (min) of MinHeap
        """
        if not self.empty():
            return self.data[0]
        return None

    def get_left_child_index(self, index: int) -> int:
        """
        Computes the index of the left child at the parent index index
        :param index: parent index
        :return: int with the left child's index (or None if no such child exists)
        """
        lc_index = (2 * index) + 1
        if lc_index < len(self):  # check if index in bounds
            return lc_index
        return None

    def get_right_child_index(self, index: int) -> int:
        """
        Computes the index of the right child at the parent index index
        :param index: parent index
        :return: int with the right child's index (or None if no such child exists)
        """
        rc_index = (2*index)+2
        if rc_index < len(self):  # check if index in bounds
            return rc_index
        return None

    def get_parent_index(self, index: int) -> int:
        """
        Computes the index of the parent at the child index
        :param index: parent index
        :return: int with the parents's index (or None if no such parent exists)
        """
        p_index = (index-1)//2
        if p_index in range(0, len(self)):  # check if index in bounds
            return p_index
        return None


    def get_min_child_index(self, index: int) -> int:
        """
        Computes the index of the child with the lower value at the parent index
        :param index: parent index
        :return: int with the minimum value child's index (or None if no children)
        """
        rc_index = self.get_right_child_index(index)
        lc_index = self.get_left_child_index(index)
        if rc_index is None and lc_index is None:
            return None
        elif rc_index is None and lc_index is not None:
            return lc_index
        elif rc_index is not None and lc_index is None:
            return rc_index
        elif self.data[rc_index] > self.data[lc_index]:
            return lc_index
        else:
            return rc_index

    def percolate_up(self, index: int) -> None:
        """
        Percolates up the value at index index to its valid spot in the heap
        :param index: index of value to be percolated up
        :return: None
        """
        parent = self.get_parent_index(index)
        if index > 0 and self.data[index] < self.data[parent]:
            self.data[index], self.data[parent] = self.data[parent], self.data[index]
            self.percolate_up(parent)

    def percolate_down(self, index: int) -> None:
        """
        Percolates down the value at index index to its valid spot in the heap
        :param index: index of value to be percolated down
        :return: None
        """
        lc = self.get_left_child_index(index)
        rc = self.get_right_child_index(index)
        if lc is not None:
            small_child = lc
            if rc is not None:
                if self.data[rc] < self.data[lc]:
                    small_child = rc
            if self.data[small_child] < self.data[index]:
                self.data[index], self.data[small_child] = self.data[small_child], self.data[index]
                self.percolate_down(small_child)


    def push(self, val: T) -> None:
        """
        Pushes the value to our heap and gets it to the proper position
        :param val: value to be added to heap
        :return None
        """
        self.data.append(val)
        self.percolate_up(len(self.data) - 1)

    def pop(self) -> T:
        """
        Removes the top element from the heap
        :return: The value that was popped
        """
        if self.empty():
            return None
        # put minimum item at the end
        self.data[0], self.data[len(self.data)-1] = self.data[len(self.data)-1], self.data[0]
        item = self.data.pop()
        self.percolate_down(0)
        return item


class MaxHeap:
    """
    Partially completed data structure. Do not modify completed portions in any way
    """
    __slots__ = ['data']

    def __init__(self):
        """
        Initializes the priority heap
        """
        self.data = MinHeap()

    def __str__(self):
        """
        Converts the priority heap to a string
        :return: string representation of the heap
        """
        return ', '.join(str(item) for item in self.data.data)

    __repr__ = __str__

    def __len__(self):
        """
        Length override function
        :return: Length of the data inside the heap
        """
        return len(self.data)

    def print_tree_format(self):
        """
        Prints heap in bfs format
        """
        self.data.to_tree_format_string()

    #   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #   Modify below this line

    def empty(self) -> bool:
        """
        Checks if the heap is empty
        :return: boolean stating if the heap is empty or not
        """
        if len(self) == 0:
            return True
        return False

    def top(self) -> int:
        """
        Returns the top value of the MaxHeap
        :return: top value of MaxHeap (maximum value)
        """
        if not self.empty():
            return self.data.data[0]*-1
        return None

    def push(self, key: int) -> None:
        """
        Pushes the value to our heap
        :param key: key to be inserted into heap
        :return: None
        """
        self.data.data.append(key*-1)
        self.data.percolate_up(len(self) - 1)

    def pop(self) -> int:
        """
        Removes the top element from the heap
        :return: value that was popped
        """
        if self.empty():
            return None
        # put minimum item at the end
        self.data.data[0], self.data.data[len(self)-1] = self.data.data[len(self)-1], self.data.data[0]
        item = self.data.data.pop()
        self.data.percolate_down(0)
        return item*-1

# This function was inspired from https://www.geeksforgeeks.org/merging-intervals/
# (resource provided in specs)
def get_eating_times(values: List[List[List[int]]]) -> List[List[int]]:
    """
    Takes in a list of interval lists such that each sublist i
    returns a list of finite-length intervals that do not
    overlap with any of the given intervals, in sorted order.
    :param values: list of interval lists
    :return: A list of non overlapping intervals
    """
    if values == []:
        return []

    # build MinHeap with time intervals
    minheap = MinHeap()
    for x in values:
        for y in x:
            minheap.push(y)

    # pop minimums from minheap to build sorted list
    sorted_intervals = []
    for n in range(len(minheap)):
        next_min = minheap.pop()
        sorted_intervals.append(next_min)

    non_overlapping = []
    merged_intervals = []
    merged_intervals.append(sorted_intervals[0])
    for i in sorted_intervals:
        start = i[0]
        if start > merged_intervals[-1][-1]:
            unique_interval = list((merged_intervals[-1][-1], i[0]))
            non_overlapping.append(unique_interval)
            merged_intervals.append(i)
        elif merged_intervals[-1][0] <= start <= merged_intervals[-1][-1]:
            merged_intervals[-1][-1] = max(merged_intervals[-1][-1], i[-1])
        else:
            merged_intervals.append(i)

    return non_overlapping
