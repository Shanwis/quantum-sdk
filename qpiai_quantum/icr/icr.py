from qpiai_quantum.circuit import QuantumRegister, ClassicalRegister
from .circuitevolution import CirucitEvolutionList
from .circuitoperation import CircuitOperation


class IntermediateCirucitRepresentation:
    """
    A representation of a quantum circuit for standardization of building and executing.
    """

    def __init__(self, *registers, name, metadata):
        """
        creates an intermediate circuit representation of the circuit holding standard information about the circuit.

        Args:
            *registers: Registers in the circuit.
            name: Name of the circuit.
            metadata: Metadata of the circuit.
        """

        self.name = name
        self.metadata = metadata
        self.qregs = [reg for reg in registers if isinstance(reg, QuantumRegister)]
        self.cregs = [reg for reg in registers if isinstance(reg, ClassicalRegister)]

        # calculate the number of qubits and classical bits
        self.num_qubits = 0
        self.num_clbits = 0

        for reg in self.qregs:
            self.num_qubits += reg.size

        for reg in self.cregs:
            self.num_clbits += reg.size

        # create the Evolution List
        self.evolve = CirucitEvolutionList()

    def _init_metadata(self):
        """
        initializes the metadata of the circuit.
        """

        self.metadata = {
            "user": {
                "id": None,
                "name": None,
                "email": None,
                "organization": None,
            },
            "circuit": {
                "id": None,
                "name": None,
            },
            "experiment": {
                "id": None,
                "name": None,
                "description": None,
            },
            "project": {
                "id": None,
                "name": None,
                "description": None,
            },
            "workspace": {
                "id": None,
                "name": None,
                "description": None,
            },
        }

    def _add_operation(self, operation: CircuitOperation):
        """
        performs the operation on the circuit.

        Args:
            operation: Operation to perform.
        """

        if not isinstance(operation, CircuitOperation):
            raise ValueError(
                "Can only perform CircuitOperation on circuit, not {}".format(
                    type(operation)
                )
            )

        self.evolve.append(operation)

    def _remove_operation(self, n: int = 1):
        """
        remove the last n nodes from the Circuit Evolution List
        """

        if n > len(self.evolve):
            raise ValueError(
                "Cannot remove {} nodes from the Circuit Evolution List".format(n)
            )

        while n > 0:
            self.evolve.pop()
            n -= 1

    def to_json(self):
        """
        Convert the circuit to json format.
        """

        return {
            "name": self.name,
            "metadata": self.metadata,
            "num_qubits": self.num_qubits,
            "num_clbits": self.num_clbits,
            "qregs": [qreg.to_json() for qreg in self.qregs],
            "cregs": [creg.to_json() for creg in self.cregs],
            "evolve": [operation.to_json() for operation in self.evolve],
        }
