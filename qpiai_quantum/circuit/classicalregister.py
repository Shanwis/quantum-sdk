from .register import Register, Bit
from .exceptions import CircuitError


class ClassicalRegister(Register):
    register_type = "Classical"

    def __init__(self, size: int, name: str = None):
        """
        An implementation of a classical register. It stores a collection of classical bits in the order they were
        added to the circuit. The bits are stored in the `bits` attribute.

        Args:
            size (int): The number of bits in the register.
            name (str): The name of the register. If not provided, a unique name is generated.
        """

        if name is None:
            name = f"creg_{id(self)}"

        super().__init__(size, name)

        self.bits = [ClBit(self, _) for _ in range(size)]

    def to_json(self):
        """
        returns the json representation of the classical register.
        """

        return {
            "name": self.name,
            "size": self.size,
            "type": self.register_type,
            "bits": [bit.to_json() for bit in self.bits],
        }

    def __str__(self):
        """
        Returns a string representation of the classical register.
        """
        return f"ClassicalRegister({self.name}, {self.size})"

    def __repr__(self):
        """
        Returns a string representation of the classical register.
        """
        return f"ClassicalRegister({self.name}, {self.size})"


class ClBit(Bit):
    def __init__(self, register, index):
        """
        An implementation of a classical bit. It is a part of a classical register.
        """

        if register is None:
            raise CircuitError("Register cannot be None.")

        if register.register_type != "Classical":
            raise CircuitError("ClBit can only be a part of a Classical Register.")

        super().__init__(register, index)

    def to_json(self):
        """
        returns the json representation of the qubit.
        """

        return {"index": self._index, "register": self._register.name}
