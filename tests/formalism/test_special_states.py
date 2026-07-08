"""Tests for SpecialStates and RandomStateGenerator."""

import unittest
import numpy as np

from qpiai_quantum.formalism.density_matrix.states import SpecialStates
from qpiai_quantum.formalism.density_matrix.random_state_generator import (
    RandomStateGenerator,
)
from qpiai_quantum.formalism.density_matrix.density_matrix import DensityMatrix


class TestWernerState(unittest.TestCase):
    """Tests for Werner state generation."""

    def test_valid_density_matrix(self):
        """Werner state should be a valid density matrix."""
        state, params = SpecialStates.werner_state(0.5)
        self.assertIsInstance(state, DensityMatrix)
        self.assertAlmostEqual(np.real(np.trace(state.state)), 1.0, places=10)
        self.assertTrue(np.allclose(state.state, state.state.conj().T, atol=1e-10))

    def test_returns_params(self):
        """Should return the seed as parameter list."""
        state, params = SpecialStates.werner_state(0.3)
        self.assertEqual(params, [0.3])

    def test_seed_zero(self):
        """Seed=0 should produce a valid state (maximally mixed)."""
        state, _ = SpecialStates.werner_state(0.0)
        self.assertAlmostEqual(np.real(np.trace(state.state)), 1.0, places=10)

    def test_seed_one(self):
        """Seed=1 should produce a valid state (Bell state)."""
        state, _ = SpecialStates.werner_state(1.0)
        self.assertAlmostEqual(np.real(np.trace(state.state)), 1.0, places=10)

    def test_invalid_seed_raises(self):
        """Seed outside [0,1] should raise."""
        with self.assertRaises(Exception):
            SpecialStates.werner_state(1.5)
        with self.assertRaises(Exception):
            SpecialStates.werner_state(-0.1)


class TestIsotropicState(unittest.TestCase):
    """Tests for isotropic state generation."""

    def test_valid_density_matrix(self):
        """Isotropic state should be a valid density matrix."""
        state = SpecialStates.isotropic_state(0.5)
        self.assertIsInstance(state, DensityMatrix)
        self.assertAlmostEqual(np.real(np.trace(state.state)), 1.0, places=10)

    def test_invalid_seed_raises(self):
        """Seed outside [0,1] should raise."""
        with self.assertRaises(Exception):
            SpecialStates.isotropic_state(2.0)


class TestMEMS(unittest.TestCase):
    """Tests for Maximally Entangled Mixed State (MEMS)."""

    def test_valid_density_matrix(self):
        """MEMS should be a valid density matrix."""
        state = SpecialStates.mems(0.42)
        self.assertIsInstance(state, DensityMatrix)
        self.assertAlmostEqual(np.real(np.trace(state.state)), 1.0, places=10)

    def test_shape(self):
        """MEMS should be 4x4 (2-qubit)."""
        state = SpecialStates.mems(0.5)
        self.assertEqual(state.state.shape, (4, 4))

    def test_hermitian(self):
        """MEMS should be Hermitian."""
        state = SpecialStates.mems(0.7)
        self.assertTrue(np.allclose(state.state, state.state.conj().T, atol=1e-10))

    def test_different_seeds_differ(self):
        """Different seeds should produce different states."""
        s1 = SpecialStates.mems(0.1)
        s2 = SpecialStates.mems(0.9)
        self.assertFalse(np.allclose(s1.state, s2.state))


class TestHaarRandomState(unittest.TestCase):
    """Tests for Haar random state generation."""

    def test_valid_density_matrix(self):
        """Haar random state should be a valid density matrix."""
        state = SpecialStates.haar_random_state(2, 0.5)
        self.assertIsInstance(state, DensityMatrix)
        self.assertAlmostEqual(np.real(np.trace(state.state)), 1.0, places=3)

    def test_shape(self):
        """Should produce correct shape for given qubit count."""
        state = SpecialStates.haar_random_state(2, 0.5)
        self.assertEqual(state.state.shape, (4, 4))

    def test_invalid_seed_raises(self):
        """Seed outside [0,1] should raise."""
        with self.assertRaises(Exception):
            SpecialStates.haar_random_state(2, 1.5)

    def test_invalid_qubits_raises(self):
        """Zero or negative qubits should raise."""
        with self.assertRaises(Exception):
            SpecialStates.haar_random_state(0, 0.5)


class TestRandomStateGenerator(unittest.TestCase):
    """Tests for RandomStateGenerator."""

    def test_generate_returns_dm_and_concurrence(self):
        """generate() should return a DensityMatrix and concurrence value."""
        rho, concurrence = RandomStateGenerator.generate(0.5, 42)
        self.assertIsInstance(rho, DensityMatrix)
        self.assertIsInstance(concurrence, (float, np.floating))

    def test_generate_valid_dm(self):
        """Generated state should be a valid density matrix."""
        rho, _ = RandomStateGenerator.generate(0.8, 123)
        self.assertAlmostEqual(np.real(np.trace(rho.state)), 1.0, places=10)
        self.assertTrue(np.allclose(rho.state, rho.state.conj().T, atol=1e-10))

    def test_generate_concurrence_range(self):
        """Concurrence should be in [0, 1]."""
        _, concurrence = RandomStateGenerator.generate(0.5, 42)
        self.assertGreaterEqual(concurrence, 0.0)
        self.assertLessEqual(concurrence, 1.0)

    def test_generate_shape(self):
        """Generated state should be 4x4 (2-qubit)."""
        rho, _ = RandomStateGenerator.generate(0.5, 42)
        self.assertEqual(rho.state.shape, (4, 4))


class TestWishart(unittest.TestCase):
    """Tests for Wishart random matrix generation."""

    def test_shape(self):
        """Should produce correct shape for given parameters."""
        result = RandomStateGenerator.wishart(2, 4, 42)
        self.assertEqual(result.shape, (4, 4))

    def test_unit_trace(self):
        """Result should have trace = 1 (normalized)."""
        result = RandomStateGenerator.wishart(2, 4, 42)
        self.assertAlmostEqual(np.real(np.trace(result)), 1.0, places=10)

    def test_positive_semidefinite(self):
        """Wishart matrix should be PSD."""
        result = RandomStateGenerator.wishart(2, 4, 42)
        eigenvalues = np.linalg.eigvalsh(result)
        self.assertTrue(np.all(eigenvalues >= -1e-10))

    def test_hermitian(self):
        """Wishart matrix should be Hermitian."""
        result = RandomStateGenerator.wishart(2, 4, 42)
        self.assertTrue(np.allclose(result, result.conj().T, atol=1e-10))

    def test_different_seeds(self):
        """Different seeds should produce different matrices."""
        r1 = RandomStateGenerator.wishart(2, 4, 1)
        r2 = RandomStateGenerator.wishart(2, 4, 2)
        self.assertFalse(np.allclose(r1, r2))


if __name__ == "__main__":
    unittest.main()
