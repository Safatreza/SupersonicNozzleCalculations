import unittest
import numpy as np
from flow_calculations import FlowCalculator

class TestFlowCalculations(unittest.TestCase):
    def setUp(self):
        self.flow_calc = FlowCalculator()
        self.gamma = 1.4  # Air
        self.R = 287.0    # J/(kg·K)

    def test_isentropic_relations(self):
        M = 2.0
        T0 = 300.0  # K
        P0 = 1e6    # Pa

        # Test temperature ratio
        T = self.flow_calc.calculate_static_temperature(T0, M, self.gamma)
        T_ratio = T0 / T
        expected_T_ratio = 1 + (self.gamma - 1) * M**2 / 2
        self.assertAlmostEqual(T_ratio, expected_T_ratio, places=5)

        # Test pressure ratio
        P = self.flow_calc.calculate_static_pressure(P0, M, self.gamma)
        P_ratio = P0 / P
        expected_P_ratio = (1 + (self.gamma - 1) * M**2 / 2)**(self.gamma / (self.gamma - 1))
        self.assertAlmostEqual(P_ratio, expected_P_ratio, places=5)

    def test_area_mach_relation(self):
        M = 2.0
        A_ratio = self.flow_calc.calculate_area_ratio(M, self.gamma)
        expected_A_ratio = 1.6875  # From isentropic tables
        self.assertAlmostEqual(A_ratio, expected_A_ratio, places=4)

    def test_mass_flow(self):
        A = 0.01  # m²
        P0 = 1e6  # Pa
        T0 = 300  # K
        M = 1.0   # Sonic flow

        m_dot = self.flow_calc.calculate_mass_flow(A, P0, T0, M, self.gamma, self.R)
        expected_m_dot = A * P0 * np.sqrt(self.gamma / (self.R * T0)) * M * (1 + (self.gamma - 1) * M**2 / 2)**(-(self.gamma + 1) / (2 * (self.gamma - 1)))
        self.assertAlmostEqual(m_dot, expected_m_dot, places=5)

    def test_thrust_calculation(self):
        m_dot = 1.0  # kg/s
        Ve = 2000.0  # m/s
        Pe = 1e5     # Pa
        Pa = 1e5     # Pa
        Ae = 0.02    # m²

        thrust = self.flow_calc.calculate_thrust(m_dot, Ve, Pe, Pa, Ae)
        expected_thrust = m_dot * Ve + (Pe - Pa) * Ae
        self.assertAlmostEqual(thrust, expected_thrust, places=5)

if __name__ == '__main__':
    unittest.main() 