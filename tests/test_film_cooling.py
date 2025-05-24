import unittest
import numpy as np
from film_cooling import FilmCoolingCalculator

class TestFilmCooling(unittest.TestCase):
    def setUp(self):
        self.film_cooling = FilmCoolingCalculator()
        
        # Test case parameters
        self.main_flow = {
            'temperature': 1000.0,  # K
            'velocity': 100.0,      # m/s
            'pressure': 1e6,        # Pa
            'density': 3.48        # kg/m³
        }
        
        self.coolant_flow = {
            'temperature': 300.0,   # K
            'velocity': 50.0,       # m/s
            'pressure': 1.2e6,      # Pa
            'density': 13.9        # kg/m³
        }
        
        self.geometry = {
            'hole_diameter': 0.005,  # m
            'hole_spacing': 0.015,   # m
            'injection_angle': 30.0, # degrees
            'length_to_diameter': 4.0
        }

    def test_blowing_ratio(self):
        BR = self.film_cooling.calculate_blowing_ratio(
            self.main_flow['density'],
            self.coolant_flow['density'],
            self.main_flow['velocity'],
            self.coolant_flow['velocity']
        )
        expected_BR = (self.coolant_flow['density'] * self.coolant_flow['velocity']) / \
                     (self.main_flow['density'] * self.main_flow['velocity'])
        self.assertAlmostEqual(BR, expected_BR, places=5)

    def test_cooling_effectiveness(self):
        x = np.array([0.1, 0.5, 1.0, 2.0])  # m
        BR = 1.0
        
        effectiveness = self.film_cooling.calculate_effectiveness(
            x,
            self.geometry['hole_diameter'],
            BR,
            self.geometry['injection_angle']
        )
        
        # Effectiveness should decrease with distance
        self.assertTrue(np.all(np.diff(effectiveness) <= 0))
        # Effectiveness should be between 0 and 1
        self.assertTrue(np.all((effectiveness >= 0) & (effectiveness <= 1)))

    def test_heat_transfer_coefficient(self):
        x = np.array([0.1, 0.5, 1.0, 2.0])  # m
        Re = 1e5
        
        h = self.film_cooling.calculate_heat_transfer_coefficient(
            x,
            self.geometry['hole_diameter'],
            Re,
            self.main_flow['velocity']
        )
        
        # Heat transfer coefficient should decrease with distance
        self.assertTrue(np.all(np.diff(h) <= 0))
        # Heat transfer coefficient should be positive
        self.assertTrue(np.all(h > 0))

    def test_wall_temperature(self):
        x = np.array([0.1, 0.5, 1.0, 2.0])  # m
        effectiveness = np.array([0.8, 0.6, 0.4, 0.2])
        
        Tw = self.film_cooling.calculate_wall_temperature(
            self.main_flow['temperature'],
            self.coolant_flow['temperature'],
            effectiveness
        )
        
        # Wall temperature should be between coolant and main flow temperatures
        self.assertTrue(np.all((Tw >= self.coolant_flow['temperature']) & 
                             (Tw <= self.main_flow['temperature'])))
        # Wall temperature should increase with distance (decreasing effectiveness)
        self.assertTrue(np.all(np.diff(Tw) >= 0))

if __name__ == '__main__':
    unittest.main() 