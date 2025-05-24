import unittest
from unittest.mock import patch
from nozzle_geometry import (
    ConvergentDivergentNozzle,
    EllipticNozzle,
    BellNozzle,
    calculate_area_ratio,
    calculate_expansion_ratio
)
import math

class TestNozzleGeometry(unittest.TestCase):
    def test_convergent_divergent_creation(self):
        nozzle = ConvergentDivergentNozzle(1.0, 2.0, 3.0)
        self.assertEqual(nozzle.throat_area, 1.0)
        self.assertEqual(nozzle.exit_area, 2.0)
        self.assertEqual(nozzle.length, 3.0)
        self.assertEqual(nozzle.convergent_angle, 30)
        self.assertEqual(nozzle.divergent_angle, 15)

    def test_elliptic_nozzle_lobes(self):
        nozzle = EllipticNozzle(1.0, 2.0, 3.0, num_lobes=6, lobe_angle=60)
        points = nozzle.get_lobe_points(1.5)
        self.assertEqual(len(points), 6)
        # Check that points are tuples of length 3
        for pt in points:
            self.assertEqual(len(pt), 3)

    def test_bell_nozzle_contour(self):
        nozzle = BellNozzle(1.0, 2.0, 3.0, wall_angle=20)
        contour = nozzle.contour_points
        self.assertEqual(len(contour), 100)
        self.assertTrue(all(isinstance(pt, tuple) and len(pt) == 2 for pt in contour))

    def test_area_ratio(self):
        nozzle = ConvergentDivergentNozzle(2.0, 8.0, 5.0)
        self.assertEqual(calculate_area_ratio(nozzle), 4.0)

    def test_expansion_ratio(self):
        nozzle = ConvergentDivergentNozzle(1.0, 2.0, 3.0)
        gamma = 1.4
        M_exit = 2.0
        ratio = calculate_expansion_ratio(nozzle, gamma, M_exit)
        self.assertTrue(isinstance(ratio, float))
        self.assertGreater(ratio, 0)

class TestMainInputHandling(unittest.TestCase):
    @patch('builtins.input', side_effect=['1', '1.0', '2.0', '3.0'])
    def test_create_nozzle_conventional(self, mock_input):
        from main import create_nozzle
        nozzle = create_nozzle()
        self.assertIsInstance(nozzle, ConvergentDivergentNozzle)

    @patch('builtins.input', side_effect=['2', '1.0', '2.0', '3.0', '6', '60'])
    def test_create_nozzle_elliptic(self, mock_input):
        from main import create_nozzle
        nozzle = create_nozzle()
        self.assertIsInstance(nozzle, EllipticNozzle)
        self.assertEqual(nozzle.num_lobes, 6)
        self.assertEqual(nozzle.lobe_angle, 60)

    @patch('builtins.input', side_effect=['3', '1.0', '2.0', '3.0', '25'])
    def test_create_nozzle_bell(self, mock_input):
        from main import create_nozzle
        nozzle = create_nozzle()
        self.assertIsInstance(nozzle, BellNozzle)
        self.assertEqual(nozzle.wall_angle, 25)

    @patch('builtins.input', side_effect=['x', '1', '1.0', '2.0', '3.0'])
    def test_create_nozzle_invalid_choice(self, mock_input):
        from main import create_nozzle
        nozzle = create_nozzle()
        self.assertIsInstance(nozzle, ConvergentDivergentNozzle)

    @patch('builtins.input', side_effect=['', '2.5'])
    def test_get_float_with_default(self, mock_input):
        from main import get_float
        val = get_float('Prompt: ', default=2.5)
        self.assertEqual(val, 2.5)

    @patch('builtins.input', side_effect=['', '7'])
    def test_get_int_with_default(self, mock_input):
        from main import get_int
        val = get_int('Prompt: ', default=7)
        self.assertEqual(val, 7)

if __name__ == '__main__':
    unittest.main() 