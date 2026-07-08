import unittest
import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from qpiai_quantum.algorithms.grover import GroverSearch
from qpiai_quantum.circuit import Circuit


class TestGroverInitializationAndCircuit(unittest.TestCase):
    def test_init(self):
        grover = GroverSearch(num_qubits=3, target="101")
        self.assertEqual(grover.num_qubits, 3)
        self.assertEqual(grover.target, "101")

    def test_invalid_target_length(self):
        grover = GroverSearch(num_qubits=3, target="11")
        with self.assertRaises(ValueError):
            grover.build_circuit()

    def test_target_missing(self):
        grover = GroverSearch(num_qubits=3)
        with self.assertRaises(ValueError):
            grover.build_circuit()

    def test_build_circuit(self):
        grover = GroverSearch(num_qubits=2, target="10")
        circuit = grover.build_circuit(iterations=1)
        self.assertIsNotNone(circuit)
        self.assertEqual(circuit.num_qubits, 2)
        self.assertEqual(circuit.num_clbits, 2)


class TestGroverMath(unittest.TestCase):
    def test_success_probability(self):
        # For N=4 (2 qubits), theta = arcsin(1/2) = pi/6
        # With 1 iteration: sin^2(3 * pi/6) = sin^2(pi/2) = 1.0
        grover = GroverSearch(num_qubits=2, target="10")
        prob = grover.get_success_probability(iterations=1)
        self.assertAlmostEqual(prob, 1.0, places=5)


@unittest.skipUnless(
    os.environ.get("RUN_ALGO_CORRECTNESS") == "1",
    "Skipping correctness test. Set RUN_ALGO_CORRECTNESS=1 to run.",
)
class TestGroverCorrectness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        api_key = os.getenv("API_KEY")
        if api_key:
            from qpiai_quantum.authentication.auth import QpiAIQuantumAuth

            try:
                QpiAIQuantumAuth.login(api_key)
            except Exception:
                pass

    def test_live_find_target_11(self):
        import uuid

        # Simplest Grover instance: 2 qubits, target "11"
        # 1 iteration finds it deterministically
        grover = GroverSearch(num_qubits=2, target="11")
        circuit = grover.build_circuit(iterations=1)
        circuit.name = f"grover_{uuid.uuid4().hex[:8]}"
        result = circuit.run(shots=100)
        counts = result.get()["counts"]

        self.assertEqual(len(counts), 1)
        self.assertIn("11", counts)
        self.assertEqual(counts["11"], 100)


if __name__ == "__main__":
    unittest.main()
