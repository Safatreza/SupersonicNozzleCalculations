import unittest
import os
import numpy as np
from cfd_integration import OpenFOAMIntegration, CFDConfig

class TestCFDIntegration(unittest.TestCase):
    def setUp(self):
        self.config = CFDConfig(
            case_name="test_case",
            mesh_type="blockMesh",
            turbulence_model="kOmegaSST",
            solver="rhoCentralFoam",
            max_iterations=1000,
            convergence_criteria=1e-6
        )
        self.cfd = OpenFOAMIntegration(self.config)
        
        # Create test directory
        self.test_dir = "test_cases/cfd_test"
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        # Clean up test directory
        if os.path.exists(self.test_dir):
            import shutil
            shutil.rmtree(self.test_dir)

    def test_mesh_generation(self):
        # Test mesh generation with Gmsh
        mesh_file = os.path.join(self.test_dir, "mesh.msh")
        self.cfd.generate_mesh(
            mesh_file,
            nozzle_length=1.0,
            throat_diameter=0.01,
            exit_diameter=0.02
        )
        self.assertTrue(os.path.exists(mesh_file))

    def test_case_setup(self):
        # Test OpenFOAM case setup
        case_dir = os.path.join(self.test_dir, "case")
        self.cfd.setup_case(
            case_dir,
            inlet_pressure=1e6,
            inlet_temperature=300,
            outlet_pressure=1e5
        )
        
        # Check if required files exist
        required_files = [
            "system/controlDict",
            "system/fvSchemes",
            "system/fvSolution",
            "0/p",
            "0/U",
            "0/T"
        ]
        for file in required_files:
            self.assertTrue(os.path.exists(os.path.join(case_dir, file)))

    def test_solver_execution(self):
        # Test solver execution
        case_dir = os.path.join(self.test_dir, "case")
        self.cfd.setup_case(
            case_dir,
            inlet_pressure=1e6,
            inlet_temperature=300,
            outlet_pressure=1e5
        )
        
        # Run solver
        success = self.cfd.run_solver(case_dir)
        self.assertTrue(success)
        
        # Check if results exist
        self.assertTrue(os.path.exists(os.path.join(case_dir, "postProcessing")))

    def test_results_processing(self):
        # Test results processing
        case_dir = os.path.join(self.test_dir, "case")
        self.cfd.setup_case(
            case_dir,
            inlet_pressure=1e6,
            inlet_temperature=300,
            outlet_pressure=1e5
        )
        
        # Run solver
        self.cfd.run_solver(case_dir)
        
        # Process results
        results = self.cfd.process_results(case_dir)
        
        # Check if results contain expected data
        self.assertIn('pressure', results)
        self.assertIn('temperature', results)
        self.assertIn('velocity', results)
        self.assertIn('mach', results)

    def test_cantera_integration(self):
        # Test Cantera integration for chemical reactions
        gas = self.cfd.setup_chemical_mechanism("gri30.cti")
        
        # Test equilibrium calculation
        gas.TP = 300, 1e5
        gas.equilibrate('TP')
        
        # Check if equilibrium calculation was successful
        self.assertTrue(gas.T > 0)
        self.assertTrue(gas.P > 0)

if __name__ == '__main__':
    unittest.main() 