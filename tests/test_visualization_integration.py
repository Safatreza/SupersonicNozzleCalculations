import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from pathlib import Path
import numpy as np
import cantera as ct
import matplotlib.pyplot as plt

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from visualization import NozzleVisualizer
from nozzle_geometry import (
    ConvergentDivergentNozzle,
    EllipticNozzle,
    BellNozzle
)

class TestVisualizationIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.test_dirs = ['output', 'output/mesh', 'output/cfd', 'output/visualization']
        for directory in self.test_dirs:
            Path(directory).mkdir(parents=True, exist_ok=True)
        
        # Create test nozzle geometries
        self.conventional_nozzle = ConvergentDivergentNozzle(0.1, 0.2, 1.0)
        self.elliptic_nozzle = EllipticNozzle(0.1, 0.2, 1.0, 4, 45)
        self.bell_nozzle = BellNozzle(0.1, 0.2, 1.0, 15)
        
        # Create test Cantera gas object
        self.gas = ct.Solution('gri30.yaml')
        self.gas.TPX = 300, 101325, 'CH4:1, O2:2, N2:7.52'
        
        # Initialize visualizer
        self.visualizer = NozzleVisualizer()

    def tearDown(self):
        """Clean up test environment"""
        plt.close('all')  # Close all matplotlib figures
        for directory in self.test_dirs:
            if os.path.exists(directory):
                for file in os.listdir(directory):
                    os.remove(os.path.join(directory, file))
                os.rmdir(directory)
        if os.path.exists('output'):
            os.rmdir('output')

    def test_gmsh_mesh_visualization(self):
        """Test Gmsh mesh visualization with different nozzle types"""
        # Create test mesh files
        mesh_files = {
            'conventional': 'output/mesh/conventional.geo',
            'elliptic': 'output/mesh/elliptic.geo',
            'bell': 'output/mesh/bell.geo'
        }
        
        for nozzle_type, mesh_file in mesh_files.items():
            # Create a simple test mesh file
            with open(mesh_file, 'w') as f:
                f.write("""
                Point(1) = {0, 0, 0, 1.0};
                Point(2) = {1, 0, 0, 1.0};
                Line(1) = {1, 2};
                """)
            
            # Test visualization
            fig = self.visualizer.visualize_gmsh_mesh(mesh_file)
            self.assertIsNotNone(fig)
            self.assertTrue(isinstance(fig, plt.Figure))
            
            # Test saving visualization
            output_file = f'output/visualization/{nozzle_type}_mesh.png'
            self.visualizer.save_visualization(output_file)
            self.assertTrue(os.path.exists(output_file))

    @patch('visualization.NozzleVisualizer.visualize_openfoam_results')
    def test_openfoam_visualization(self, mock_visualize):
        """Test OpenFOAM results visualization"""
        # Create test OpenFOAM case directory
        cfd_dir = 'output/cfd'
        os.makedirs(cfd_dir, exist_ok=True)
        
        # Test visualization
        self.visualizer.visualize_openfoam_results(cfd_dir)
        mock_visualize.assert_called_once_with(cfd_dir)

    def test_cantera_visualization(self):
        """Test Cantera results visualization"""
        # Test visualization
        fig = self.visualizer.visualize_cantera_results(self.gas)
        self.assertIsNotNone(fig)
        self.assertTrue(isinstance(fig, plt.Figure))
        
        # Test saving visualization
        output_file = 'output/visualization/cantera_results.png'
        self.visualizer.save_visualization(output_file)
        self.assertTrue(os.path.exists(output_file))

    def test_visualization_error_handling(self):
        """Test error handling in visualization functions"""
        # Test with non-existent mesh file
        with self.assertRaises(Exception):
            self.visualizer.visualize_gmsh_mesh('nonexistent.geo')
        
        # Test with non-existent OpenFOAM case
        with self.assertRaises(Exception):
            self.visualizer.visualize_openfoam_results('nonexistent_case')
        
        # Test with invalid Cantera gas object
        with self.assertRaises(Exception):
            self.visualizer.visualize_cantera_results(None)

    def test_visualization_options(self):
        """Test visualization options and parameters"""
        # Test Gmsh mesh visualization with options
        mesh_file = 'output/mesh/test.geo'
        with open(mesh_file, 'w') as f:
            f.write("""
            Point(1) = {0, 0, 0, 1.0};
            Point(2) = {1, 0, 0, 1.0};
            Line(1) = {1, 2};
            """)
        
        fig = self.visualizer.visualize_gmsh_mesh(
            mesh_file,
            show_streamlines=True,
            show_contours=True
        )
        self.assertIsNotNone(fig)
        
        # Test Cantera visualization with options
        fig = self.visualizer.visualize_cantera_results(
            self.gas,
            show_heat_release=True,
            show_species=True
        )
        self.assertIsNotNone(fig)

if __name__ == '__main__':
    unittest.main() 