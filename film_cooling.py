import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple
from enum import Enum

class CoolantType(Enum):
    """Types of coolants supported for film cooling"""
    AIR = "air"
    HELIUM = "helium"
    NEON = "neon"

@dataclass
class CoolantProperties:
    """Properties of different coolants"""
    name: CoolantType
    specific_heat: float  # J/kg·K
    thermal_conductivity: float  # W/m·K
    viscosity: float  # Pa·s
    density: float  # kg/m³

# Coolant property database
COOLANT_PROPERTIES: Dict[CoolantType, CoolantProperties] = {
    CoolantType.AIR: CoolantProperties(
        name=CoolantType.AIR,
        specific_heat=1005.0,
        thermal_conductivity=0.0262,
        viscosity=1.84e-5,
        density=1.225
    ),
    CoolantType.HELIUM: CoolantProperties(
        name=CoolantType.HELIUM,
        specific_heat=5193.0,
        thermal_conductivity=0.1513,
        viscosity=1.97e-5,
        density=0.1786
    ),
    CoolantType.NEON: CoolantProperties(
        name=CoolantType.NEON,
        specific_heat=1030.0,
        thermal_conductivity=0.0491,
        viscosity=3.13e-5,
        density=0.8999
    )
}

@dataclass
class InjectionConfig:
    """Configuration for coolant injection"""
    angle: float  # degrees from wall
    slot_height: float  # meters
    slot_width: float  # meters
    blowing_ratio: float  # ratio of coolant to mainstream momentum
    coolant_type: CoolantType
    coolant_temp: float  # Kelvin
    coolant_velocity: float  # m/s

class FilmCoolingAnalysis:
    """Analysis of film cooling effectiveness"""
    def __init__(self, injection_config: InjectionConfig):
        self.config = injection_config
        self.coolant_props = COOLANT_PROPERTIES[injection_config.coolant_type]
        
    def calculate_effectiveness(self, x: float, main_temp: float, main_velocity: float) -> float:
        """
        Calculate film cooling effectiveness at a given distance from injection
        
        Args:
            x: Distance from injection point (m)
            main_temp: Mainstream temperature (K)
            main_velocity: Mainstream velocity (m/s)
            
        Returns:
            Effectiveness (η) between 0 and 1
        """
        # Calculate momentum ratio
        momentum_ratio = (self.config.blowing_ratio * 
                        (self.coolant_props.density / COOLANT_PROPERTIES[CoolantType.AIR].density) *
                        (self.config.coolant_velocity / main_velocity) ** 2)
        
        # Calculate dimensionless distance
        x_plus = x / self.config.slot_height
        
        # Calculate effectiveness using empirical correlation
        # Based on Goldstein's correlation with modifications for injection angle
        angle_factor = np.cos(np.radians(self.config.angle))
        effectiveness = 1.9 * momentum_ratio ** 0.2 * x_plus ** (-0.2) * angle_factor
        
        # Ensure effectiveness is between 0 and 1
        return max(0.0, min(1.0, effectiveness))
    
    def calculate_wall_temperature(self, x: float, main_temp: float, main_velocity: float) -> float:
        """
        Calculate wall temperature at a given distance from injection
        
        Args:
            x: Distance from injection point (m)
            main_temp: Mainstream temperature (K)
            main_velocity: Mainstream velocity (m/s)
            
        Returns:
            Wall temperature (K)
        """
        effectiveness = self.calculate_effectiveness(x, main_temp, main_velocity)
        return main_temp - effectiveness * (main_temp - self.config.coolant_temp)
    
    def calculate_heat_transfer_coefficient(self, x: float, main_velocity: float) -> float:
        """
        Calculate heat transfer coefficient at a given distance from injection
        
        Args:
            x: Distance from injection point (m)
            main_velocity: Mainstream velocity (m/s)
            
        Returns:
            Heat transfer coefficient (W/m²·K)
        """
        # Calculate Reynolds number
        Re = (main_velocity * x * COOLANT_PROPERTIES[CoolantType.AIR].density / 
              COOLANT_PROPERTIES[CoolantType.AIR].viscosity)
        
        # Calculate Nusselt number using modified correlation
        Nu = 0.0296 * Re ** 0.8 * (self.config.blowing_ratio ** 0.2)
        
        # Calculate heat transfer coefficient
        return Nu * COOLANT_PROPERTIES[CoolantType.AIR].thermal_conductivity / x

def analyze_cooling_performance(injection_config: InjectionConfig, 
                              x_points: List[float],
                              main_temp: float,
                              main_velocity: float) -> Dict[str, List[float]]:
    """
    Analyze film cooling performance at multiple points
    
    Args:
        injection_config: Configuration for coolant injection
        x_points: List of distances from injection point to analyze
        main_temp: Mainstream temperature (K)
        main_velocity: Mainstream velocity (m/s)
        
    Returns:
        Dictionary containing effectiveness, wall temperature, and heat transfer coefficient
        at each x position
    """
    analysis = FilmCoolingAnalysis(injection_config)
    
    results = {
        'effectiveness': [],
        'wall_temperature': [],
        'heat_transfer_coefficient': []
    }
    
    for x in x_points:
        results['effectiveness'].append(
            analysis.calculate_effectiveness(x, main_temp, main_velocity))
        results['wall_temperature'].append(
            analysis.calculate_wall_temperature(x, main_temp, main_velocity))
        results['heat_transfer_coefficient'].append(
            analysis.calculate_heat_transfer_coefficient(x, main_velocity))
    
    return results 