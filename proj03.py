
from typing import TypeVar, List

# for more information on type hinting, check out https://docs.python.org/3/library/typing.html
T = TypeVar("T")  # represents generic type
Node = TypeVar("Node")  # represents a Node object (forward-declare to use in Node __init__)
DLL = TypeVar("DLL")


# pro tip: PyCharm auto-renders docstrings (the multiline strings under each function definition)
# in its "Documentation" view when written in the format we use here. Open the "Documentation"
# view to quickly see what a function does by placing your cursor on it and using CTRL + Q.
# https://www.jetbrains.com/help/pycharm/documentation-tool-window.html


class Node:
    """
    Implementation of a doubly linked list node.
    Do not modify.
    """
    __slots__ = ["value", "next", "prev"]

    def __init__(self, value: T, next: Node = None, prev: Node = None) -> None:
        """
        Construct a doubly linked list node.

        :param value: value held by the Node.
        :param next: reference to the next Node in the linked list.
        :param prev: reference to the previous Node in the linked list.
        :return: None.
        """
        self.next = next
        self.prev = prev
        self.value = value

    def __repr__(self) -> str:
        """
        Represents the Node as a string.

        :return: string representation of the Node.
        """
        return f"Node({str(self.value)})"

    def __eq__(self, other: Node):
        return self.value == other.value

    __str__ = __repr__


class DLL:
    """
    Implementation of a doubly linked list without padding nodes.
    Modify only below indicated line.
    """
    __slots__ = ["head", "tail", "size"]

    def __init__(self) -> None:
        """
        Construct an empty doubly linked list.

        :return: None.
        """
        self.head = self.tail = None
        self.size = 0

    def __repr__(self) -> str:
        """
        Represent the DLL as a string.

        :return: string representation of the DLL.
        """
        result = []
        node = self.head
        while node is not None:
            result.append(str(node))
            node = node.next
            if node is self.head:
                break
        return " <-> ".join(result)

    def __str__(self) -> str:
        """
        Represent the DLL as a string.

        :return: string representation of the DLL.
        """
        return repr(self)

    def __eq__(self, other: DLL) -> bool:
        """
        :param other: compares equality with this List
        :return: True if equal otherwise False
        """
        cur_node = self.head
        other_node = other.head
        while True:
            if cur_node != other_node:
                return False
            if cur_node is None and other_node is None:
                return True
            if cur_node is None or other_node is None:
                return False
            cur_node = cur_node.next
            other_node = other_node.next
            if cur_node is self.head and other_node is other.head:
                return True
            if cur_node is self.head or other_node is other.head:
                return False

    # MODIFY BELOW #
    # Refer to the classes provided to understand the problems better#

    def empty(self) -> bool:
        """
        Determines if DLL is empty or not.
        :return: boolean indicating whether the DLL is empty
        """
        if self.head is None:
            return True
        else:
            return False

    def push(self, val: T, back: bool = True) -> None:
        """
        Adds a Node containing val to the back
        (or front) of the DLL and updates size accordingly
        :param val: T: value to added to DLL
        :param back: bool: If True, add val to the back of the DLL. If False, add to the front
        :return: None
        """
        new_node = Node(val)
        if back == True:   # push to back of DLL
            if self.head is None:  # DLL is empty
                self.head = new_node
                self.tail = new_node
            else:
                self.tail.next = new_node
                new_node.prev = self.tail
                self.tail = new_node
        else:        # push to front of DLL
            if self.head is None:   # DLL is empty
                self.head = new_node
                self.tail = new_node
            else:
                new_node.next = self.head
                self.head.prev = new_node
                self.head = new_node


    def pop(self, back: bool = True) -> None:
        """
        Removes a Node from the back (or front)
        of the DLL and updates size accordingly
        :param back: bool: If True, remove from the back of the DLL.
        If False, remove from the front.
        :return None
        """
        if self.empty() == True:  # check for empty DLL
            return False
        else:
            if self.head == self.tail:  # only one node left
                self.head = None
                self.tail = None
            elif back == True:  # remove from back of DLL
                if self.tail.prev is not None:
                    self.tail.prev.next = None
                self.tail = self.tail.prev
            else:    # remove from front of DLL
                if self.head.next is not None:
                    self.head.next.prev = None
                self.head = self.head.next


    def list_to_dll(self, source: List[T]) -> None:
        """
        Creates a DLL from a standard Python list
        :param source: Standard Python list from which to construct DLL.
        :return None
        """
        # clear DLL
        self.head = None
        self.tail = None

        for item in source:
            self.push(item)

    def dll_to_list(self) -> List[T]:
        """
        Creates a standard Python list from a DLL
        :return list[T] containing the values of the nodes in the DLL.
        """
        py_list = []
        curr = self.head
        while curr is not None:
            py_list.append(curr.value)
            curr = curr.next

        return py_list

    def _find_nodes(self, val: T, find_first: bool = False) -> List[Node]:
        """
        Construct list of Nodes with value val in the DLL
        and returns the associated Node object list
        :param val: Value to be found in the DLL
        :param find_first:  if True find only the first element in the DLL,
        if False find all instances of the elements in the DLL
        :return list of Node objects in the DLL whose value is val.
        If val does not exist in the DLL, returns empty list
        """
        nodes_w_val = []
        curr = self.head
        while curr is not None:
            if curr.value == val:
                nodes_w_val.append(curr)
                if find_first == True:
                    break
            curr = curr.next

        return nodes_w_val

    def find(self, val: T) -> Node:
        """
        Finds first Node with value val in the DLL
        and returns the associated Node object.
        :param val: T: Value to be found in the DLL
        :return first Node object in the DLL whose value is val.
        If val does not exist in the DLL, returns None.
        """
        found_nodes = self._find_nodes(val, find_first = True)
        if len(found_nodes) == 0:
            return None
        else:
            return found_nodes[0]

    def find_all(self, val: T) -> List[Node]:
        """
        Finds all Node objects with value val in the DLL
        and returns a standard Python list of the associated Node objects
        :param val: T: Value to be found in the DLL
        :return  Python list of all Node objects in the DLL whose value is val.
        If val does not exist in the DLL, returns an empty list.
        """
        found_nodes = self._find_nodes(val)
        return found_nodes

    def _remove_node(self, to_remove: Node) -> None:
        """
        Given a reference to a node in the linked list this function will remove it
        :param to_remove: Node: Node to be removed from the DLL
        :return None
        """
        succ = to_remove.next
        pred = to_remove.prev

        if succ is not None:
            succ.prev = pred
        if pred is not None:
            pred.next = succ
        if to_remove is self.head:
            self.head = succ
        if to_remove is self.tail:
            self.tail = pred

    def remove(self, val: T) -> bool:
        """
        Removes first Node with value val in the DLL
        :param val: T: Value to be removed from the DLL
        :return True if a Node with value val was found and
        removed from the DLL, else False
        """
        node_to_remove = self.find(val)
        if node_to_remove is None:
            return False
        else:
            self._remove_node(node_to_remove)
            return True

    def remove_all(self, val: T) -> int:
        """
        Removes all Node objects with value val in the DLL
        :param val: T: Value to be removed from the DLL
        :return number of Node objects with value val removed from the DLL.
        If no node containing val exists in the DLL, returns 0
        """
        nodes_to_remove = self.find_all(val)
        for cur_node in nodes_to_remove:
            self._remove_node(cur_node)
        return len(nodes_to_remove)

    # This function was partly inspired from this source
    # https://stackoverflow.com/questions/11166968/reversing-a-doubly-linked-list
    def reverse(self) -> None:
        """
        Reverses the DLL in-place
        :return None
        """
        curr = self.tail
        while curr is not None:
            next_node = curr.next
            curr.next = curr.prev
            curr.prev = next_node
            curr = curr.next

        # swap head and tail nodes
        tail_node = self.tail
        self.tail = self.head
        self.head = tail_node


def fix_playlist(lst: DLL) -> bool:
    """
    Correct the given playlists by either fixing the linked lists
    that do not make a cycle or by identifying the linked lists that
    create incorrect circular dependencies
    :param lst: DLL music playlist that potentially has problems
    :return bool indicating proper, broken or improper linked list
    If proper or broken, it will return True. If improper, it will return False
    """

    def connect_list() -> None:
        """
        Fixes broken list by implementing a proper cycle
        :return: None
        """
        # make tail's next pointer point to head
        lst.tail.next = lst.head
        # make heads prev pointer point to tail
        lst.head.prev = lst.tail

    def fix_playlist_helper(slow: Node, fast: Node) -> int:
        """
        Checks if the given lst is proper(1), broken(2), or improper(3)
        :param slow: node that will move through list one node at a time
        :param fast: node that will move through list two nodes at a time
        :return
        """
        while (fast is not None) and (fast.next is not None) and (slow.next is not None):
            if fast == slow:  # has cycle
                if slow.next == lst.head:  # proper cycle
                    return 1
                else:           # improper cycle
                    return 3
            fast = fast.next.next
            slow = slow.next
        return 2  # no cycle: Broken

    if lst.head is None:  # empty list: proper
        return True
    fast_node = lst.head.next
    slow_node = lst.head

    dll_type = fix_playlist_helper(slow_node, fast_node)
    if dll_type == 1:  # proper cycle
        return True
    elif dll_type == 2:   # broken cycle
        connect_list()
        return True
    elif dll_type == 3:  # improper cycle
        return False







