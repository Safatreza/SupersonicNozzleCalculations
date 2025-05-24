import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QLineEdit, QComboBox, QPushButton,
    QGroupBox, QFormLayout, QDoubleSpinBox, QSpinBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from nozzle_geometry import (
    ConvergentDivergentNozzle,
    EllipticNozzle,
    BellNozzle,
    calculate_area_ratio,
    calculate_expansion_ratio
)
from film_cooling import (
    CoolantType,
    InjectionConfig,
    analyze_cooling_performance
)
from cfd_integration import (
    OpenFOAMIntegration,
    create_cfd_config
)

class NozzleCanvas(FigureCanvas):
    """Canvas for displaying nozzle geometry and flow properties"""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        
    def plot_nozzle(self, nozzle, flow_data=None):
        """Plot nozzle geometry and flow properties"""
        self.axes.clear()
        
        if isinstance(nozzle, ConvergentDivergentNozzle):
            self._plot_convergent_divergent(nozzle)
        elif isinstance(nozzle, EllipticNozzle):
            self._plot_elliptic(nozzle)
        elif isinstance(nozzle, BellNozzle):
            self._plot_bell(nozzle)
            
        if flow_data:
            self._plot_flow_properties(flow_data)
            
        self.axes.set_xlabel('Axial Position (m)')
        self.axes.set_ylabel('Radius (m)')
        self.axes.grid(True)
        self.fig.tight_layout()
        self.draw()
        
    def _plot_convergent_divergent(self, nozzle):
        """Plot convergent-divergent nozzle geometry"""
        x = np.linspace(0, nozzle.length, 100)
        r = np.zeros_like(x)
        
        # Convergent section
        conv_mask = x < nozzle.length * 0.3
        r[conv_mask] = nozzle.exit_area + (nozzle.throat_area - nozzle.exit_area) * (1 - x[conv_mask] / (nozzle.length * 0.3))
        
        # Divergent section
        div_mask = ~conv_mask
        r[div_mask] = nozzle.throat_area + (nozzle.exit_area - nozzle.throat_area) * (x[div_mask] - nozzle.length * 0.3) / (nozzle.length * 0.7)
        
        self.axes.plot(x, r, 'b-', label='Nozzle Wall')
        self.axes.plot(x, -r, 'b-')
        
    def _plot_elliptic(self, nozzle):
        """Plot elliptic nozzle geometry"""
        x = np.linspace(0, nozzle.length, 100)
        theta = np.linspace(0, 2*np.pi, 100)
        
        for i in range(nozzle.num_lobes):
            angle = 2 * np.pi * i / nozzle.num_lobes
            r = nozzle.throat_area + (nozzle.exit_area - nozzle.throat_area) * (x / nozzle.length)
            x_3d = x
            y_3d = r * np.cos(theta + angle)
            z_3d = r * np.sin(theta + angle)
            
            self.axes.plot(x_3d, y_3d, 'b-', alpha=0.5)
            self.axes.plot(x_3d, z_3d, 'b-', alpha=0.5)
            
    def _plot_bell(self, nozzle):
        """Plot bell nozzle geometry"""
        x = np.linspace(0, nozzle.length, 100)
        a = (nozzle.exit_area - nozzle.throat_area) / (nozzle.length ** 3)
        r = nozzle.throat_area + a * (x ** 3)
        
        self.axes.plot(x, r, 'b-', label='Nozzle Wall')
        self.axes.plot(x, -r, 'b-')
        
    def _plot_flow_properties(self, flow_data):
        """Plot flow properties (temperature, pressure, velocity)"""
        x = flow_data['x']
        for prop, values in flow_data.items():
            if prop != 'x':
                self.axes.plot(x, values, '--', label=prop)
        self.axes.legend()

class MainWindow(QMainWindow):
    """Main window for the nozzle analysis tool"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Supersonic Nozzle Analysis Tool")
        self.setMinimumSize(1200, 800)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # Create left panel for inputs
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Create tabs for different input sections
        tabs = QTabWidget()
        
        # Nozzle geometry tab
        geometry_tab = QWidget()
        geometry_layout = QFormLayout(geometry_tab)
        
        self.nozzle_type = QComboBox()
        self.nozzle_type.addItems(["Convergent-Divergent", "Elliptic", "Bell-shaped"])
        geometry_layout.addRow("Nozzle Type:", self.nozzle_type)
        
        self.throat_area = QDoubleSpinBox()
        self.throat_area.setRange(0.001, 10.0)
        self.throat_area.setValue(0.01)
        self.throat_area.setSuffix(" m²")
        geometry_layout.addRow("Throat Area:", self.throat_area)
        
        self.exit_area = QDoubleSpinBox()
        self.exit_area.setRange(0.001, 10.0)
        self.exit_area.setValue(0.02)
        self.exit_area.setSuffix(" m²")
        geometry_layout.addRow("Exit Area:", self.exit_area)
        
        self.nozzle_length = QDoubleSpinBox()
        self.nozzle_length.setRange(0.1, 10.0)
        self.nozzle_length.setValue(1.0)
        self.nozzle_length.setSuffix(" m")
        geometry_layout.addRow("Nozzle Length:", self.nozzle_length)
        
        # Flow conditions tab
        flow_tab = QWidget()
        flow_layout = QFormLayout(flow_tab)
        
        self.t_static = QDoubleSpinBox()
        self.t_static.setRange(200, 3000)
        self.t_static.setValue(300)
        self.t_static.setSuffix(" K")
        flow_layout.addRow("Static Temperature:", self.t_static)
        
        self.m_inlet = QDoubleSpinBox()
        self.m_inlet.setRange(0.1, 5.0)
        self.m_inlet.setValue(0.5)
        flow_layout.addRow("Inlet Mach Number:", self.m_inlet)
        
        self.m_exit = QDoubleSpinBox()
        self.m_exit.setRange(1.0, 10.0)
        self.m_exit.setValue(2.0)
        flow_layout.addRow("Exit Mach Number:", self.m_exit)
        
        self.p_total = QDoubleSpinBox()
        self.p_total.setRange(100000, 10000000)
        self.p_total.setValue(1000000)
        self.p_total.setSuffix(" Pa")
        flow_layout.addRow("Total Pressure:", self.p_total)
        
        # Film cooling tab
        cooling_tab = QWidget()
        cooling_layout = QFormLayout(cooling_tab)
        
        self.coolant_type = QComboBox()
        self.coolant_type.addItems(["Air", "Helium", "Neon"])
        cooling_layout.addRow("Coolant Type:", self.coolant_type)
        
        self.injection_angle = QDoubleSpinBox()
        self.injection_angle.setRange(0, 90)
        self.injection_angle.setValue(30)
        self.injection_angle.setSuffix(" °")
        cooling_layout.addRow("Injection Angle:", self.injection_angle)
        
        self.blowing_ratio = QDoubleSpinBox()
        self.blowing_ratio.setRange(0.1, 5.0)
        self.blowing_ratio.setValue(1.0)
        cooling_layout.addRow("Blowing Ratio:", self.blowing_ratio)
        
        # Add tabs to tab widget
        tabs.addTab(geometry_tab, "Nozzle Geometry")
        tabs.addTab(flow_tab, "Flow Conditions")
        tabs.addTab(cooling_tab, "Film Cooling")
        
        left_layout.addWidget(tabs)
        
        # Add analyze button
        analyze_button = QPushButton("Analyze")
        analyze_button.clicked.connect(self.analyze)
        left_layout.addWidget(analyze_button)
        
        # Create right panel for visualization
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Add canvas for nozzle visualization
        self.canvas = NozzleCanvas(right_panel)
        right_layout.addWidget(self.canvas)
        
        # Add results display
        self.results_label = QLabel()
        self.results_label.setFont(QFont("Courier", 10))
        right_layout.addWidget(self.results_label)
        
        # Add panels to main layout
        layout.addWidget(left_panel, 1)
        layout.addWidget(right_panel, 2)
        
    def analyze(self):
        """Perform nozzle analysis and update visualization"""
        try:
            # Create nozzle geometry
            nozzle_type = self.nozzle_type.currentText()
            if nozzle_type == "Convergent-Divergent":
                nozzle = ConvergentDivergentNozzle(
                    self.throat_area.value(),
                    self.exit_area.value(),
                    self.nozzle_length.value()
                )
            elif nozzle_type == "Elliptic":
                nozzle = EllipticNozzle(
                    self.throat_area.value(),
                    self.exit_area.value(),
                    self.nozzle_length.value()
                )
            else:  # Bell-shaped
                nozzle = BellNozzle(
                    self.throat_area.value(),
                    self.exit_area.value(),
                    self.nozzle_length.value()
                )
            
            # Calculate flow properties
            gamma = 1.4  # Default value
            cp = 1005.0  # Default value
            
            T0 = calc_total_temperature(self.t_static.value(), self.m_inlet.value(), gamma)
            Te = calc_static_exit_temperature(T0, self.m_exit.value(), gamma)
            Ve = calc_exit_velocity(cp, T0, Te)
            Pe = calc_pressure_ratio(self.m_exit.value(), gamma) * self.p_total.value()
            
            # Create flow data for visualization
            x = np.linspace(0, nozzle.length, 100)
            flow_data = {
                'x': x,
                'Temperature': np.linspace(T0, Te, 100),
                'Pressure': np.linspace(self.p_total.value(), Pe, 100),
                'Velocity': np.linspace(0, Ve, 100)
            }
            
            # Update visualization
            self.canvas.plot_nozzle(nozzle, flow_data)
            
            # Display results
            results_text = f"""
Results:
--------
Total Temperature: {T0:.2f} K
Exit Temperature: {Te:.2f} K
Exit Velocity: {Ve:.2f} m/s
Exit Pressure: {Pe:.2f} Pa
Area Ratio: {calculate_area_ratio(nozzle):.2f}
"""
            self.results_label.setText(results_text)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 