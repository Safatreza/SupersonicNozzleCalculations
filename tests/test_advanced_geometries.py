import unittest
import numpy as np
from nozzle_geometry import BellNozzle, TrumpetNozzle, ScarfedNozzle

class TestAdvancedGeometries(unittest.TestCase):
    def setUp(self):
        self.bell_nozzle = BellNozzle(
            throat_area=0.01,
            exit_area=0.02,
            length=1.0,
            expansion_ratio=15.0,
            wall_angle=15.0
        )
        
        self.trumpet_nozzle = TrumpetNozzle(
            throat_area=0.01,
            exit_area=0.02,
            length=1.0,
            curvature_radius=0.2
        )
        
        self.scarfed_nozzle = ScarfedNozzle(
            throat_area=0.01,
            exit_area=0.02,
            length=1.0,
            scarf_angle=30.0
        )

    def test_bell_nozzle_contour(self):
        x = np.linspace(0, 1.0, 100)
        y = self.bell_nozzle.calculate_contour(x)
        
        # Check contour properties
        self.assertEqual(len(y), 100)
        self.assertTrue(np.all(y >= 0))  # No negative radii
        self.assertTrue(np.all(np.diff(y) >= 0))  # Monotonically increasing

    def test_trumpet_nozzle_contour(self):
        x = np.linspace(0, 1.0, 100)
        y = self.trumpet_nozzle.calculate_contour(x)
        
        # Check contour properties
        self.assertEqual(len(y), 100)
        self.assertTrue(np.all(y >= 0))
        self.assertTrue(np.all(np.diff(y) >= 0))

    def test_scarfed_nozzle_contour(self):
        x = np.linspace(0, 1.0, 100)
        y = self.scarfed_nozzle.calculate_contour(x)
        
        # Check contour properties
        self.assertEqual(len(y), 100)
        self.assertTrue(np.all(y >= 0))
        
        # Check scarf angle effect
        exit_angle = np.arctan2(y[-1] - y[-2], x[-1] - x[-2])
        self.assertAlmostEqual(np.degrees(exit_angle), self.scarfed_nozzle.scarf_angle, places=1)

    def test_flow_area_calculation(self):
        x = np.linspace(0, 1.0, 100)
        
        # Test bell nozzle
        bell_areas = self.bell_nozzle.calculate_area(x)
        self.assertTrue(np.all(bell_areas >= self.bell_nozzle.throat_area))
        self.assertTrue(np.all(bell_areas <= self.bell_nozzle.exit_area))
        
        # Test trumpet nozzle
        trumpet_areas = self.trumpet_nozzle.calculate_area(x)
        self.assertTrue(np.all(trumpet_areas >= self.trumpet_nozzle.throat_area))
        self.assertTrue(np.all(trumpet_areas <= self.trumpet_nozzle.exit_area))
        
        # Test scarfed nozzle
        scarfed_areas = self.scarfed_nozzle.calculate_area(x)
        self.assertTrue(np.all(scarfed_areas >= self.scarfed_nozzle.throat_area))
        self.assertTrue(np.all(scarfed_areas <= self.scarfed_nozzle.exit_area))

    def test_geometric_properties(self):
        # Test bell nozzle
        self.assertAlmostEqual(self.bell_nozzle.expansion_ratio, 15.0)
        self.assertAlmostEqual(self.bell_nozzle.wall_angle, 15.0)
        
        # Test trumpet nozzle
        self.assertAlmostEqual(self.trumpet_nozzle.curvature_radius, 0.2)
        
        # Test scarfed nozzle
        self.assertAlmostEqual(self.scarfed_nozzle.scarf_angle, 30.0)

if __name__ == '__main__':
    unittest.main() 