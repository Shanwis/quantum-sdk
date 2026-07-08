from .register import Register, Bit
from .exceptions import CircuitError


class Qubit(Bit):
    def __init__(self, register, index):
        """
        Implementation of a Qubit which is a part of a Quantum Register.

        Args:
            register (QuantumRegister): The quantum register to which the qubit belongs.
            index (int): The index of the qubit in the register
        """

        if register is None:
            raise CircuitError("Register cannot be None.")

        if register.register_type != "Quantum":
            raise CircuitError("Qubit can only be a part of a Quantum Register.")

        super().__init__(register, index)

    def to_json(self):
        """
        returns the json representation of the qubit.
        """

        return {"index": self._index, "register": self._register.name}


class QuantumRegister(Register):
    register_type = "Quantum"

    def __init__(self, size: int, name: str = None):
        """
        Implements a QuantumRegister which stores the name and size of the register.

        Args:
            size (int): The number of qubits in the register.
            name (str): The name of the register. If not provided, a unique name is generated.
        """

        if name is None:
            name = f"qreg_{id(self)}"
        super().__init__(size, name)

        self.bits = [Qubit(self, i) for i in range(size)]

    def to_json(self):
        """
        returns the json representation of the quantum register.
        """

        return {
            "name": self.name,
            "size": self.size,
            "type": self.register_type,
            "bits": [bit.to_json() for bit in self.bits],
        }

    def __str__(self):
        """
        Returns a string representation of the quantum register.
        """
        return f"QuantumRegister({self.name}, {self.size})"

    def __repr__(self):
        """
        Returns a string representation of the quantum register.
        """
        return f"QuantumRegister({self.name}, {self.size})"
