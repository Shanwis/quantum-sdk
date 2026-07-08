import numpy as np
from .density_matrix import DensityMatrix


class RandomStateGenerator:
    @staticmethod
    def generate(mixedness: float, seed: float):
        """
        Generate a random state
        """

        np.random.seed(seed)

        concurrence = np.random.uniform(0, 1)
        theta = 0.5 * np.arcsin(concurrence)
        phi = np.random.uniform(0, 2 * np.pi)

        non_MES = [
            [
                (np.cos(theta) ** 2),
                0,
                0,
                (np.exp(-1j * phi) * np.sin(theta) * np.cos(theta)),
            ],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [
                (np.exp(1j * phi) * np.sin(theta) * np.cos(theta)),
                0,
                0,
                (np.sin(theta) ** 2),
            ],
        ]

        ent_state = np.array([[mixedness * value for value in row] for row in non_MES])
        noise = np.array(
            [
                [((1 - mixedness) / 4) * value for value in row]
                for row in [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
            ]
        )

        state = np.add(ent_state, noise)
        rho = DensityMatrix(state)

        return rho, np.real(concurrence)

    @staticmethod
    def wishart(n: int, s: int, seed: float):
        np.random.seed(seed)

        def RandomGinibre(d: int, s: int):
            """Creates a random complex Ginibre matrix of size d x s"""
            X = (np.random.randn(d, s) + 1.0j * np.random.randn(d, s)) / np.sqrt(2)
            return X

        def RandomWishart(d: int, s: int):
            """Creates a sample from the Wishart ensemble of parameters (d,s). The resulting matrix is PSD of size d x d"""
            X = RandomGinibre(d, s)
            W = np.matmul(X, X.conj().transpose())
            return W

        d = 2**n
        flag = RandomWishart(d, s)
        flag = np.array(flag / np.trace(flag))
        return flag
