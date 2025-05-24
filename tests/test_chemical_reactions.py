import unittest
import numpy as np
import cantera as ct
from chemical_reactions import ChemicalReactionCalculator

class TestChemicalReactions(unittest.TestCase):
    def setUp(self):
        self.chem_calc = ChemicalReactionCalculator()
        self.gas = ct.Solution('gri30.yaml')
        
        # Test case parameters
        self.initial_state = {
            'T': 300.0,  # K
            'P': 101325.0,  # Pa
            'X': {
                'CH4': 0.1,
                'O2': 0.2,
                'N2': 0.7
            }
        }

    def test_equilibrium_calculation(self):
        # Test equilibrium calculation
        self.gas.TP = self.initial_state['T'], self.initial_state['P']
        self.gas.X = self.initial_state['X']
        
        # Calculate equilibrium
        self.gas.equilibrate('TP')
        
        # Check if equilibrium was reached
        self.assertTrue(self.gas.T > 0)
        self.assertTrue(self.gas.P > 0)
        self.assertTrue(np.all(self.gas.X >= 0))
        self.assertAlmostEqual(np.sum(self.gas.X), 1.0)

    def test_reaction_rates(self):
        # Test reaction rate calculation
        self.gas.TP = self.initial_state['T'], self.initial_state['P']
        self.gas.X = self.initial_state['X']
        
        # Calculate reaction rates
        rates = self.chem_calc.calculate_reaction_rates(self.gas)
        
        # Check reaction rates
        self.assertTrue(np.all(rates >= 0))
        self.assertEqual(len(rates), self.gas.n_reactions)

    def test_species_production_rates(self):
        # Test species production rate calculation
        self.gas.TP = self.initial_state['T'], self.initial_state['P']
        self.gas.X = self.initial_state['X']
        
        # Calculate production rates
        prod_rates = self.chem_calc.calculate_production_rates(self.gas)
        
        # Check production rates
        self.assertEqual(len(prod_rates), self.gas.n_species)
        self.assertTrue(np.all(np.isfinite(prod_rates)))

    def test_heat_release(self):
        # Test heat release calculation
        self.gas.TP = self.initial_state['T'], self.initial_state['P']
        self.gas.X = self.initial_state['X']
        
        # Calculate heat release
        heat_release = self.chem_calc.calculate_heat_release(self.gas)
        
        # Check heat release
        self.assertTrue(np.isfinite(heat_release))
        self.assertTrue(heat_release >= 0)

    def test_ignition_delay(self):
        # Test ignition delay calculation
        self.gas.TP = self.initial_state['T'], self.initial_state['P']
        self.gas.X = self.initial_state['X']
        
        # Calculate ignition delay
        delay = self.chem_calc.calculate_ignition_delay(self.gas)
        
        # Check ignition delay
        self.assertTrue(np.isfinite(delay))
        self.assertTrue(delay >= 0)

    def test_species_concentrations(self):
        # Test species concentration calculation
        self.gas.TP = self.initial_state['T'], self.initial_state['P']
        self.gas.X = self.initial_state['X']
        
        # Calculate species concentrations
        conc = self.chem_calc.calculate_species_concentrations(self.gas)
        
        # Check concentrations
        self.assertEqual(len(conc), self.gas.n_species)
        self.assertTrue(np.all(conc >= 0))

if __name__ == '__main__':
    unittest.main() 