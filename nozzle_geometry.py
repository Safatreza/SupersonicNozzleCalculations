import numpy as np
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class NozzleGeometry:
    """Base class for nozzle geometries"""
    throat_area: float
    exit_area: float
    length: float

class ConvergentDivergentNozzle(NozzleGeometry):
    """Conventional convergent-divergent nozzle"""
    def __init__(self, throat_area: float, exit_area: float, length: float):
        super().__init__(throat_area, exit_area, length)
        self.convergent_angle = 30  # degrees
        self.divergent_angle = 15   # degrees

class EllipticNozzle(NozzleGeometry):
    """Elliptic nozzle with sharp-tipped lobes"""
    def __init__(self, throat_area: float, exit_area: float, length: float,
                 num_lobes: int = 4, lobe_angle: float = 45):
        super().__init__(throat_area, exit_area, length)
        self.num_lobes = num_lobes
        self.lobe_angle = lobe_angle  # degrees

    def get_lobe_points(self, x: float) -> List[Tuple[float, float]]:
        """Calculate points for the elliptic lobes at a given x position"""
        points = []
        for i in range(self.num_lobes):
            angle = 2 * np.pi * i / self.num_lobes
            # Calculate radius based on x position (linear interpolation)
            r = self.throat_area + (self.exit_area - self.throat_area) * (x / self.length)
            x_point = x
            y_point = r * np.cos(angle)
            z_point = r * np.sin(angle)
            points.append((x_point, y_point, z_point))
        return points

class BellNozzle(NozzleGeometry):
    """Bell-shaped nozzle for flat-top density profiles"""
    def __init__(self, throat_area: float, exit_area: float, length: float,
                 wall_angle: float = 15):
        super().__init__(throat_area, exit_area, length)
        self.wall_angle = wall_angle  # degrees
        self.contour_points = self._generate_contour()

    def _generate_contour(self) -> List[Tuple[float, float]]:
        """Generate the bell nozzle contour using a polynomial curve"""
        x = np.linspace(0, self.length, 100)
        # Use a 3rd order polynomial for the contour
        a = (self.exit_area - self.throat_area) / (self.length ** 3)
        y = self.throat_area + a * (x ** 3)
        return list(zip(x, y))

def calculate_area_ratio(nozzle: NozzleGeometry) -> float:
    """Calculate the area ratio (exit area / throat area)"""
    return nozzle.exit_area / nozzle.throat_area

def calculate_expansion_ratio(nozzle: NozzleGeometry, gamma: float, M_exit: float) -> float:
    """Calculate the required expansion ratio for a given exit Mach number"""
    return ((1 + ((gamma - 1) / 2) * M_exit**2) / ((gamma + 1) / 2)) ** ((gamma + 1) / (2 * (gamma - 1))) 