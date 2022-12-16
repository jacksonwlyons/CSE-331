from typing import TypeVar, Tuple  # For use in type hinting

# Type Declarations
T = TypeVar('T')  # generic type
SLL = TypeVar('SLL')  # forward declared
Node = TypeVar('Node')  # forward declare `Node` type


class SLLNode:
    """
    Node implementation
    Do not modify.
    """

    __slots__ = ['val', 'next']

    def __init__(self, value: T, next: Node = None) -> None:
        """
        Initialize an SLL Node
        :param value: value held by node
        :param next: reference to the next node in the SLL
        :return: None
        """
        self.val = value
        self.next = next

    def __str__(self) -> str:
        """
        Overloads `str()` method to cast nodes to strings
        return: string
        """
        return '(Node: ' + str(self.val) + ' )'

    def __repr__(self) -> str:
        """
        Overloads `repr()` method for use in debugging
        return: string
        """
        return '(Node: ' + str(self.val) + ' )'

    def __eq__(self, other: Node) -> bool:
        """
        Overloads `==` operator to compare nodes
        :param other: right operand of `==`
        :return: bool
        """
        return self is other if other is not None else False


class RecursiveSinglyLinkedList:
    """
    Recursive implementation of an SLL
    """

    __slots__ = ['head', 'tail']

    def __init__(self) -> None:
        """
        Initializes an SLL
        :return: None
        """
        self.head = None
        self.tail = None

    def __repr__(self) -> str:
        """
        Represents an SLL as a string
        """
        return self.to_string(self.head)

    def __eq__(self, other: SLL) -> bool:
        """
        Overloads `==` operator to compare SLLs
        :param other: right hand operand of `==`
        :return: `True` if equal, else `False`
        """
        comp = lambda n1, n2: n1 == n2 and (comp(n1.next, n2.next) if (n1 and n2) else True)
        return comp(self.head, other.head)

    # ============ Modify below ============ #

    def push(self, value: T, back: bool = True) -> None:
        """
        Inserts an SLLNode at the end of the list if back
        is true. Otherwise it will insert the node at the front
        :param value: value to push to the list
        :param back: bool True/False to insert at front vs. end of list
        :return: None
        """

        node = SLLNode(value)
        if back == True:
            if self.head == None:
                self.head = node
                self.tail = node
            else:
                self.tail.next = node
                self.tail = node
        else:
            if self.head == None:
                self.head = node
                self.tail = node
            else:
                node.next = self.head
                self.head = node

    def to_string(self, curr: Node) -> str:
        """
        Converts an SLL to a string
        :param curr: current node which starts at head of SLL
        :return: string representation of the linked list
        """

        if (curr != None) and (curr.next != None):
            return str(curr.val) + " --> " + self.to_string(curr.next)
        elif (curr != None):
            return str(curr.val)
        else:
            return "None"

    def length(self, curr: Node) -> int:
        """
        Determines number of nodes in the list starting at head curr
        :param curr: current node which starts at head of SLL
        :return: int number of nodes in list
        """

        if (curr != None) and (curr.next != None):
            return (1 + self.length(curr.next))
        elif (curr != None):
            return 1
        else:
            return 0

    def sum_list(self, curr: Node) -> T:
        """
        Sums the values in the list
        :param curr: current node which starts at head of SLL
        :return: sum of values in list
        """
        if (curr != None) and (curr.next != None):
            return (curr.val + self.sum_list(curr.next))
        elif (curr != None):
            return curr.val
        else:
            return None

    def search(self, value: T) -> bool:
        """
        Searches the SLL for a node containing `value`
        :param value: value to search for
        :return: `True` if found, else `False`
        """

        def search_inner(curr: Node) -> bool:
            """
            Looks for value (from search) in the list starting at head curr
            :param curr: current node which starts at head of SLL
            :return: `True` if found, else `False`
            """
            if (curr != None) and (curr.next != None):
                if curr.val == value:
                    return True
                else:
                    return search_inner(curr.next)
            elif (curr != None) and (curr.val == value):
                return True
            else:
                return False

        return search_inner(self.head)

    def count(self, value: T) -> int:
        """
        Returns the number of occurrences of `value` in this list
        :param value: value to count
        :return: number of times the value occurred
        """

        def count_inner(curr: Node) -> int:
            """
            Counts and returns how many times the given value
            occurs in the list starting at head curr
            :param curr: current node which starts at head of SLL
            :return: number of times the value occurred
            """
            if (curr != None) and (curr.next != None):
                if curr.val == value:
                    return (1 + count_inner(curr.next))
                else:
                    return count_inner(curr.next)
            elif (curr != None) and (curr.val == value):
                return 1
            else:
                return 0

        return count_inner(self.head)

    def remove(self, value: T) -> bool:
        """
        Removes the first node containing `value` from the SLL
        :param value: value to remove
        :return: True if a node was removed, False otherwise
        """

        def remove_inner(curr: Node) -> Tuple[Node, bool]:
            """
            Remove the first node in the list with the
            given value (from remove) starting at head curr
            :param curr: current node which starts at head of SLL
            :return: tuple with the head of the list and bool indicating
            if anything was successfully deleted
            """

            if self.head == None:
                return (self.head, False)
            elif curr == None:
                return (self.head, False)
            else:
                # check head, remove node if it is value
                if self.head.val == value:
                    self.head = self.head.next
                    # check if the last node was removed. aka list is now empty
                    if self.head == None:
                        self.tail = None
                    return (self.head, True)
                elif (curr != None) and (curr.next != None):
                    if curr.next.next == None:
                        # check last node in list
                        if curr.next.val == value:
                            curr.next = curr.next.next
                            self.tail = curr
                            return (self.head, True)
                        else:
                            return (self.head, False)
                    # check next node
                    elif curr.next.val == value:
                        curr.next = curr.next.next
                        return (self.head, True)
                    # node hasn't been found yet, call func again with next node
                    else:
                        return remove_inner(curr.next)
                # value not in list
                else:
                    return (self.head, False)

        head_node, removed_bool = remove_inner(self.head)
        return removed_bool

    def remove_all(self, value: T) -> bool:
        """
        Removes all nodes in the list with the given value
        :param value: value to remove
        :return: True if a node was removed, False otherwise
        """

        def remove_all_inner(curr: Node) -> Tuple[Node, bool]:
            """
            Removes all nodes in the list with the given value
            (from remove_all) starting at head curr
            :param curr: current node which starts at head of SLL
            :return: tuple with the head of the list and bool indicating
            if anything was successfully deleted
            """
            if self.head == None:
                return (self.head, False)
            elif curr == None:
                return (self.head, False)
            else:
                # check head, remove node if it is value
                if self.head.val == value:
                    self.head = self.head.next
                    # check if the last node was removed. aka list is now empty
                    if self.head == None:
                        self.tail = None
                    remove_all_inner(curr.next)
                    return (self.head, True)
                elif (curr != None) and (curr.next != None):
                    if curr.next.next == None:
                        # check last node in list
                        if curr.next.val == value:
                            curr.next = curr.next.next
                            self.tail = curr
                            return (self.head, True)
                        else:
                            return (self.head, False)
                    # check next node
                    elif curr.next.val == value:
                        curr.next = curr.next.next
                        remove_all_inner(curr.next)
                        return (self.head, True)
                    # node hasn't been found yet, call func again with next node
                    else:
                        return remove_all_inner(curr.next)
                # value not in list
                else:
                    return (self.head, False)

        head_node, removed_bool = remove_all_inner(self.head)
        return removed_bool


def reverse(data: SLL, curr: Node) -> None:
    """
    Reverses the data
    :param data: an SLL
    :param curr: current node which starts at head of SLL
    :return: None
    """
    # base cases
    # Assign tail to be head
    data.tail = data.head
    if (curr == None):
        return None
    else:
        next_node = curr.next
    # check for end of list
    if next_node == None:
        # assign last node in list to be head
        data.head = curr
        return None
    # recursive call: go to next node
    reverse(data, next_node)
    # starting from end of list, essentially change direction of arrows
    # Make the next node after curr point back to curr
    next_node.next = curr
    # remove pointer from curr to next node
    curr.next = None
