from typing import TypeVar  # For use in type hinting

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
        # return self.val == other.val if other is not None else False


class SinglyLinkedList:
    """
    Implementation of an SLL
    """

    __slots__ = ['head', 'tail']

    def __init__(self) -> None:
        """
        Initializes an SLL
        :return: None
        DO NOT MODIFY THIS FUNCTION
        """
        self.head = None
        self.tail = None

    def __repr__(self) -> str:
        """
        Represents an SLL as a string
        DO NOT MODIFY THIS FUNCTION
        """
        return self.to_string()

    def __eq__(self, other: SLL) -> bool:
        """
        Overloads `==` operator to compare SLLs
        :param other: right hand operand of `==`
        :return: `True` if equal, else `False`
        DO NOT MODIFY THIS FUNCTION
        """
        comp = lambda n1, n2: n1 == n2 and (comp(n1.next, n2.next) if (n1 and n2) else True)
        return comp(self.head, other.head)

    # ============ Modify below ============ #
    def push(self, value: T) -> None:
        """
        Pushes an SLLNode to the end of the list
        :param value: value to push to the list
        :return: None
        """

        node = SLLNode(value)
        if self.head == None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

# WRITE YOUR CODE HERE
    def to_string(self) -> str:
        """
        Converts an SLL to a string
        :return: string representation of the linked list
        """

        SLL_str = ""
        if self.head == None:
            return "None"
        else:
            current_node = self.head
            while current_node.next != None:
                SLL_str += current_node.val + " --> "
                current_node = current_node.next
            SLL_str += current_node.val
        return SLL_str

# WRITE YOUR CODE HERE

    def length(self) -> int:
        """
        Determines number of nodes in the list
        :return: number of nodes in list
        """

        SLL_len = 0
        if self.head == None:
            return 0
        else:
            current_node = self.head
            while current_node != None:
                SLL_len += 1
                current_node = current_node.next
        return SLL_len

# WRITE YOUR CODE HERE

    def sum_list(self) -> T:
        """
        Sums the values in the list
        :return: sum of values in list
        """

        if self.head == None:
            return None
        else:
            current_node = self.head
            # check type of nodes
            if type(current_node.val) == int:
                SLL_sum = 0
            else:
                SLL_sum = ""
            while current_node != None:
                SLL_sum += current_node.val
                current_node = current_node.next
        return SLL_sum

# WRITE YOUR CODE HERE

    def remove(self, value: T) -> bool:
        """
        Removes the first node containing `value` from the SLL
        :param value: value to remove
        :return: True if a node was removed, False otherwise
        """
        if self.head == None:
            return False
        else:
            current_node = self.head
            while current_node != None:
                # check if current node is at the end of SLL
                if current_node.next == None:
                    if current_node.val == value:
                        self.head = None
                        self.tail = None
                        return True
                    else:
                        return False
                # check next node
                if current_node.next.val == value:
                    if current_node.next.next == None:
                        self.tail = current_node
                    current_node.next = current_node.next.next
                    return True
                # check if current node is at the front of SLL
                if current_node.val == value:
                    self.head = self.head.next
                current_node = current_node.next

        return False


# WRITE YOUR CODE HERE

    def remove_all(self, value: T) -> bool:
        """
        Removes all instances of a node containing `value` from the SLL
        :param value: value to remove
        :return: True if a node was removed, False otherwise
        """

        nodes_removed = False
        # SLL is empty
        if self.head == None:
            return False
        else:
            # Remove nodes w/ val from head
            while self.head.val == value:
                self.head = self.head.next
                nodes_removed = True
                if self.head == None:
                    break
            current_node = self.head
            # Remove nodes w/ val from middle and tail
            while current_node != None:
                if current_node.next != None:
                    if current_node.next.val == value:
                        if current_node.next.next == None:
                            self.tail = current_node
                        current_node.next = current_node.next.next
                        nodes_removed = True
                else:
                    break
                current_node = current_node.next
        # SLL is empty
        if self.head == None:
            self.tail = None
        if nodes_removed != False:
            return True
        else:
            return False

    # WRITE YOUR CODE HERE

    def search(self, value: T) -> bool:
        """
        Searches the SLL for a node containing `value`
        :param value: value to search for
        :return: `True` if found, else `False`
        """

        current_node = self.head
        while current_node != None:
            if current_node.val == value:
                return True
            current_node = current_node.next

        return False

# WRITE YOUR CODE HERE

    def count(self, value: T) -> int:
        """
        Returns the number of occurrences of `value` in this list
        :param value: value to count
        :return: number of times the value occurred
        """
        count = 0
        current_node = self.head
        while current_node != None:
            if current_node.val == value:
                count += 1
            current_node = current_node.next

        return count

    # new function I created to help write my reverse function
    def prepend(self, value):
        """
        This function will create a new node with the given value
        and prepend this node to the SLL.
        :param value: value of new node to be prepended to SLL
        :return: None
        """
        new_node = SLLNode(value)
        if self.head == None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node


def reverse(data: SLL) -> None:
    """
    Reverses the data
    :param data: an SLL
    :return: None
    """
    temp_SLL = SinglyLinkedList()
    current_node = data.head
    # prepend each node from data SLL to temp_SLL
    while current_node != None:
        temp_SLL.prepend(current_node.val)
        current_node = current_node.next
    # clear data SLL
    data.head = None
    data.tail = None
    # push nodes from temp_SLL to data SLL
    current_node2 = temp_SLL.head
    while current_node2 != None:
        data.push(current_node2.val)
        current_node2 = current_node2.next



