import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from pathlib import Path
import numpy as np
import cantera as ct

# Add parent directory to path to import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import (
    get_float,
    get_int,
    create_nozzle,
    get_cooling_config,
    get_cfd_config,
    setup_output_directories
)

class TestMain(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.test_dirs = ['output', 'output/mesh', 'output/cfd', 'output/visualization']
        
    def tearDown(self):
        """Clean up test environment"""
        for directory in self.test_dirs:
            if os.path.exists(directory):
                for file in os.listdir(directory):
                    os.remove(os.path.join(directory, file))
                os.rmdir(directory)
        if os.path.exists('output'):
            os.rmdir('output')

    @patch('builtins.input', side_effect=['1.5', 'invalid', '2.0'])
    def test_get_float(self, mock_input):
        """Test get_float function with valid and invalid inputs"""
        result = get_float("Enter a number: ")
        self.assertEqual(result, 1.5)
        result = get_float("Enter a number: ")
        self.assertEqual(result, 2.0)

    @patch('builtins.input', side_effect=['5', 'invalid', '10'])
    def test_get_int(self, mock_input):
        """Test get_int function with valid and invalid inputs"""
        result = get_int("Enter an integer: ")
        self.assertEqual(result, 5)
        result = get_int("Enter an integer: ")
        self.assertEqual(result, 10)

    @patch('builtins.input', side_effect=['1', '0.1', '0.2', '1.0'])
    def test_create_nozzle_conventional(self, mock_input):
        """Test creating a conventional nozzle"""
        nozzle = create_nozzle()
        self.assertEqual(nozzle.__class__.__name__, 'ConvergentDivergentNozzle')
        self.assertEqual(nozzle.throat_area, 0.1)
        self.assertEqual(nozzle.exit_area, 0.2)
        self.assertEqual(nozzle.length, 1.0)

    @patch('builtins.input', side_effect=['2', '0.1', '0.2', '1.0', '4', '45'])
    def test_create_nozzle_elliptic(self, mock_input):
        """Test creating an elliptic nozzle"""
        nozzle = create_nozzle()
        self.assertEqual(nozzle.__class__.__name__, 'EllipticNozzle')
        self.assertEqual(nozzle.throat_area, 0.1)
        self.assertEqual(nozzle.exit_area, 0.2)
        self.assertEqual(nozzle.length, 1.0)
        self.assertEqual(nozzle.num_lobes, 4)
        self.assertEqual(nozzle.lobe_angle, 45)

    @patch('builtins.input', side_effect=['3', '0.1', '0.2', '1.0', '15'])
    def test_create_nozzle_bell(self, mock_input):
        """Test creating a bell nozzle"""
        nozzle = create_nozzle()
        self.assertEqual(nozzle.__class__.__name__, 'BellNozzle')
        self.assertEqual(nozzle.throat_area, 0.1)
        self.assertEqual(nozzle.exit_area, 0.2)
        self.assertEqual(nozzle.length, 1.0)
        self.assertEqual(nozzle.wall_angle, 15)

    @patch('builtins.input', side_effect=['1', '30', '0.001', '0.01', '0.5', '300', '100'])
    def test_get_cooling_config(self, mock_input):
        """Test getting cooling configuration"""
        config = get_cooling_config()
        self.assertEqual(config.angle, 30)
        self.assertEqual(config.slot_height, 0.001)
        self.assertEqual(config.slot_width, 0.01)
        self.assertEqual(config.blowing_ratio, 0.5)
        self.assertEqual(config.coolant_temp, 300)
        self.assertEqual(config.coolant_velocity, 100)

    @patch('builtins.input', side_effect=['100', '1', '1', '1000', '1e-6', '1e-6', '0.1'])
    def test_get_cfd_config(self, mock_input):
        """Test getting CFD configuration"""
        config = get_cfd_config()
        self.assertEqual(config['mesh_resolution'], 100)
        self.assertEqual(config['turbulence_model'], 'kEpsilon')
        self.assertEqual(config['wall_treatment'], 'wallFunction')
        self.assertEqual(config['max_iterations'], 1000)
        self.assertEqual(config['convergence_criteria'], 1e-6)
        self.assertEqual(config['time_step'], 1e-6)
        self.assertEqual(config['end_time'], 0.1)

    def test_setup_output_directories(self):
        """Test setting up output directories"""
        setup_output_directories()
        for directory in self.test_dirs:
            self.assertTrue(os.path.exists(directory))
            self.assertTrue(os.path.isdir(directory))

if __name__ == '__main__':
    unittest.main() 