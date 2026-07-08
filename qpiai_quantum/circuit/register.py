from .exceptions import CircuitError


class Register:
    """
    Base class which provides an implementation of a generic register.
    Super class for :class:`~.ClassicalRegister` and :class:`~.QuantumRegister`.
    """

    def __init__(self, size: int, name: str = None):
        """
        creates a register with the bit size of `size` and names it as `name`.
        """

        if name is None:
            name = f"reg{id(self)}"

        # Type validation
        if not isinstance(size, int):
            raise CircuitError("Size of a register must be an integer.")

        if not isinstance(name, str):
            raise CircuitError("Cannot keep a non-string as name for a register")

        # Value validation
        if size <= 0:
            raise CircuitError("Size of a register must be greater than 0.")
        if name == "":
            raise CircuitError("Name of a register cannot be empty.")

        self._size = size
        self._name = name

    def __str__(self):
        return f"Register({self.name}, {self.size})"

    def __repr__(self):
        return f"Register({self.name}, {self.size})"

    def __eq__(self, other):
        if not isinstance(other, Register):
            return False
        return self.size == other.size and self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def size(self):
        """
        Returns the size of the register.
        """
        return self._size

    @size.setter
    def size(self, size):
        """
        Sets the size of the register.
        """
        self._size = size

    @property
    def name(self):
        """
        Returns the name of the register.
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of the register.
        """
        self._name = name


class Bit:
    """
    A class to implement a generic bit
    Super class for :class:`~.ClBit` and :class:`~.Qubit`

    All gates and measurements are applied to a bit. This bit is stored in a register at some index
    """

    def __init__(self, register: Register, index: int):
        """
        Defines a bit in a register at some index.

        args:
            register: Register
                The register in which the bit is defined.
            index: int
                The index of the bit in the register.
        """
        self._register = register
        self._index = index
