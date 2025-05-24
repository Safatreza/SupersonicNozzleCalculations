import unittest
import numpy as np
from nozzle_geometry import NozzleGeometry, ConvergentDivergentNozzle, EllipticNozzle, LobedNozzle

class TestNozzleGeometry(unittest.TestCase):
    def setUp(self):
        self.cd_nozzle = ConvergentDivergentNozzle(
            throat_area=0.01,
            exit_area=0.02,
            length=1.0
        )
        self.elliptic_nozzle = EllipticNozzle(
            throat_area=0.01,
            exit_area=0.02,
            length=1.0,
            aspect_ratio=2.0
        )
        self.lobed_nozzle = LobedNozzle(
            throat_area=0.01,
            exit_area=0.02,
            length=1.0,
            num_lobes=4
        )

    def test_area_ratio(self):
        self.assertAlmostEqual(self.cd_nozzle.area_ratio, 2.0)
        self.assertAlmostEqual(self.elliptic_nozzle.area_ratio, 2.0)
        self.assertAlmostEqual(self.lobed_nozzle.area_ratio, 2.0)

    def test_area_calculation(self):
        x = np.linspace(0, 1.0, 100)
        areas = self.cd_nozzle.calculate_area(x)
        self.assertEqual(len(areas), 100)
        self.assertTrue(np.all(areas >= self.cd_nozzle.throat_area))

    def test_elliptic_geometry(self):
        x = np.linspace(0, 1.0, 100)
        areas = self.elliptic_nozzle.calculate_area(x)
        self.assertTrue(np.all(areas >= self.elliptic_nozzle.throat_area))
        self.assertTrue(np.all(areas <= self.elliptic_nozzle.exit_area))

    def test_lobed_geometry(self):
        x = np.linspace(0, 1.0, 100)
        areas = self.lobed_nozzle.calculate_area(x)
        self.assertTrue(np.all(areas >= self.lobed_nozzle.throat_area))
        self.assertTrue(np.all(areas <= self.lobed_nozzle.exit_area))

if __name__ == '__main__':
    unittest.main() 