class EvolutionNode:
    """
    Generic node, representing an abstract operation made on the circuit at some point.
    """

    def __init__(self, operation=None, prev=None, next=None):
        """
        Create a new node for operation in the circuit evolution.

        Args:
            operation (CiricitOperation): the operation to be performed on the circuit / gate application
            prev (EvolutionNode): the previous operation in the evolution.
            next (EvolutionNode): the next operation in the evolution.

        Defaults:
            prev: None
            next: None
        """

        if operation is None:
            raise Exception("Cannot creation a evolution node without an operation")

        self.operation = operation
        self.prev = prev
        self.next = next


class CirucitEvolutionList:
    """
    Data Sructure to hold operate on the circuit evolution.
    """

    def __init__(self):
        """
        Create a new Evolution list with null as head and tail by default. Size of list set to 0
        """

        self.head = None
        self.tail = None
        self.size = 0

    def _create_head_with_operation(self, operation):
        """
        Create and initialize the head of the linked list on first operation
        """

        # create a head and tail and set tail pointer to head
        self.head = EvolutionNode(operation)
        self.tail = self.head
        self.size += 1

    def append_to_tail(self, operation):
        """
        append a operation to the end of the evolution linked list
        """

        if self.size == 0:
            self._create_head_with_operation(operation)
            return

        # create a dummy node
        node = EvolutionNode(operation)

        # tail next is dummy
        self.tail.next = node

        # node prev is tail
        node.prev = self.tail

        # node will be tai;
        self.tail = node

        self.size += 1

    def append_to_head(self, operation):
        """
        append a operation to the start of the evolution linked list
        """
        if self.size == 0:
            self._create_head_with_operation(operation)
            return

        # create a dummy node
        node = EvolutionNode(operation)

        # node next is current head
        node.next = self.head

        # current head prev is node
        self.head.prev = node

        # set node to head
        self.head = node

        self.size += 1

    def append(self, operation):
        """
        append a operation to the end of the evolution linked list (same as append_to_tail)
        """
        self.append_to_tail(operation)
        return

    def pop_tail(self):
        """
        remove the operation at the end of the evolution linked list
        """

        if self.size <= 0:
            raise Exception("No operation to pop from tail.")

        # hold onto the tail just in case
        node = self.tail
        new_tail = node.prev

        if new_tail is not None:
            new_tail.next = None
        else:
            self.head = None

        # push the tail back
        self.tail = new_tail

        self.size -= 1

    def pop_head(self):
        """
        remove the operation at the start of the evolution linked list
        """

        if self.size <= 0:
            raise Exception("No operation to pop from head")

        new_head = self.head.next

        if new_head is not None:
            new_head.prev = None
        else:
            self.tail = None

        # push the head forward
        self.head = new_head

        self.size -= 1

    def pop(self):
        """
        remove the operation at the end of the evolution linked list (same as pop_tail)
        """
        self.pop_tail()
        return

    def __len__(self):
        """
        return the size of the evolution linked list
        """
        return self.size

    def __list__(self):
        """
        return the list representation of the evolution linked list
        """

        if self.size == 0:
            return "Empty evolution list"

        current = self.head
        result = []
        while current is not None:
            result.append(current.operation)
            current = current.next

        return result

    def __iter__(self):
        """
        return the iterator representation of the evolution linked list
        """

        if self.size == 0:
            return iter([])

        current = self.head
        while current is not None:
            yield current.operation
            current = current.next

    def __str__(self):
        """
        return the string representation of the evolution linked list
        """

        if self.size == 0:
            return "Empty evolution list"

        current = self.head
        result = []
        while current is not None:
            result.append(current.operation)
            current = current.next

        return str(result)

    def __repr__(self):
        """
        return the string representation of the evolution linked list
        """
        return f"CircuitEvolutionList({self.size})"
