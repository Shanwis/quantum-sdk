import numpy as np


class GateMatrices:
    def RZ(theta):
        return np.array(
            [
                [np.cos(theta / 2) - 1j * np.sin(theta / 2), 0],
                [0, np.cos(theta / 2) + 1j * np.sin(theta / 2)],
            ],
            dtype=np.complex128,
        )

    def RY(theta):
        return np.array(
            [
                [np.cos(theta / 2), -np.sin(theta / 2)],
                [np.sin(theta / 2), np.cos(theta / 2)],
            ],
            dtype=np.complex128,
        )
