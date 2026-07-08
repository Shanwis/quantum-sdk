from .circuitoperation import CircuitOperation, OperationType


class CustomControlOperation(CircuitOperation):
    """
    For a given operation this will transform the operation into a controlled operation.
    """

    def __init__(self, *control: int, operation: CircuitOperation):
        for control_qubit in control:
            if not isinstance(control_qubit, int):
                raise ValueError("Control qubit must be an integer")
            if control_qubit in operation.qubits:
                raise ValueError("Control qubit already in operation qubits")

        if (
            operation.operation_type == OperationType.BARRIER
            or operation.operation_type == OperationType.MEASURE
        ):
            raise ValueError(
                f"Operation {operation.gate_name} cannot be controlled by another qubit"
            )

        super().__init__(
            operation.operation_type,
            f"C{operation.gate_name}",
            [*control, *operation.qubits],
            operation.params,
            operation.clbits,
        )
