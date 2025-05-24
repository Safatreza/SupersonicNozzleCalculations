import unittest
import numpy as np
import matplotlib.pyplot as plt
import cantera as ct
from pathlib import Path
from visualization import NozzleVisualizer

class TestVisualization(unittest.TestCase):
    def setUp(self):
        self.visualizer = NozzleVisualizer()
        self.test_dir = Path('test_output')
        self.test_dir.mkdir(exist_ok=True)
        
        # Create test gas object
        self.gas = ct.Solution('gri30.yaml')
        self.gas.TP = 300.0, 101325.0
        self.gas.X = {'CH4': 0.1, 'O2': 0.2, 'N2': 0.7}

    def test_gmsh_visualization(self):
        # Test Gmsh visualization
        geo_file = 'examples/gmsh/nozzle.geo'
        fig = self.visualizer.visualize_gmsh_mesh(geo_file, show_mesh=False)
        
        # Check if figure was created
        self.assertIsNotNone(fig)
        self.assertIsInstance(fig, plt.Figure)
        
        # Save visualization
        output_file = self.test_dir / 'gmsh_mesh.png'
        self.visualizer.save_visualization(str(output_file))
        self.assertTrue(output_file.exists())

    def test_cantera_visualization(self):
        # Test Cantera visualization
        fig = self.visualizer.visualize_cantera_results(self.gas)
        
        # Check if figure was created
        self.assertIsNotNone(fig)
        self.assertIsInstance(fig, plt.Figure)
        
        # Check if axes were created
        self.assertEqual(len(fig.axes), 2)
        
        # Save visualization
        output_file = self.test_dir / 'cantera_results.png'
        self.visualizer.save_visualization(str(output_file))
        self.assertTrue(output_file.exists())

    def test_openfoam_visualization(self):
        # Test OpenFOAM visualization
        case_dir = 'examples/openfoam'
        output_file = self.visualizer.visualize_openfoam_results(case_dir)
        
        # Check if output file exists
        self.assertTrue(Path(output_file).exists())

    def tearDown(self):
        # Clean up test files
        for file in self.test_dir.glob('*.png'):
            file.unlink()
        self.test_dir.rmdir()

if __name__ == '__main__':
    unittest.main() 