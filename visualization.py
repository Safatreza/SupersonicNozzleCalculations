import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import gmsh
import cantera as ct
import os
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QComboBox, QLabel, 
                            QFileDialog, QTabWidget, QMessageBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from typing import Optional, List, Dict, Any, Union
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

class NozzleVisualizer:
    def __init__(self):
        """Initialize the NozzleVisualizer"""
        self.fig = None
        self.ax = None
        self.animation = None
        self.velocity_data = None
        
    def _get_velocity_data(self):
        """Get velocity data for streamlines"""
        if self.velocity_data is None:
            # Create synthetic velocity data for testing
            x = np.linspace(0, 1, 50)
            y = np.linspace(0, 1, 50)
            X, Y = np.meshgrid(x, y)
            self.velocity_data = {
                'u': np.ones_like(X),
                'v': np.zeros_like(Y)
            }
        return self.velocity_data
        
    def visualize_gmsh_mesh(self, mesh_file: str, show_streamlines: bool = False,
                          show_contours: bool = False, view_3d: bool = False) -> Optional[plt.Figure]:
        """Visualize Gmsh mesh with optional streamlines and contours"""
        try:
            gmsh.initialize()
            gmsh.open(mesh_file)
            gmsh.model.mesh.generate(2)  # Generate 2D mesh
            
            # Get mesh data
            nodes = gmsh.model.mesh.getNodes()
            elements = gmsh.model.mesh.getElements(2)
            
            # Create figure
            self.fig = plt.figure(figsize=(10, 8))
            if view_3d:
                self.ax = self.fig.add_subplot(111, projection='3d')
            else:
                self.ax = self.fig.add_subplot(111)
            
            # Plot mesh
            x = nodes[1][0::3]
            y = nodes[1][1::3]
            z = nodes[1][2::3]
            
            if view_3d:
                self.ax.plot_trisurf(x, y, z, triangles=elements[1][0]-1, cmap='viridis')
                self.ax.set_zlabel('Z')
            else:
                self.ax.triplot(x, y, elements[1][0]-1, 'k-', alpha=0.5)
            
            self.ax.set_xlabel('X')
            self.ax.set_ylabel('Y')
            self.ax.set_title('Nozzle Mesh')
            
            if show_streamlines:
                self._add_streamlines(x, y, z)
            
            if show_contours:
                self._add_contours(x, y, z)
            
            plt.tight_layout()
            return self.fig
            
        except Exception as e:
            print(f"Error visualizing mesh: {str(e)}")
            return None
        finally:
            gmsh.finalize()

    def visualize_openfoam_results(self, case_dir: str, time_step: str = 'latest',
                                 show_3d: bool = False) -> None:
        """Visualize OpenFOAM results using ParaView"""
        try:
            # Create ParaView script
            script = f"""
            from paraview.simple import *
            case = OpenFOAMReader(FileName='{case_dir}/system/controlDict')
            case.MeshRegions = ['internalMesh']
            case.CellArrays = ['U', 'p', 'T']
            
            if '{time_step}' == 'latest':
                case.TimestepValues = case.TimestepValues[-1]
            else:
                case.TimestepValues = {time_step}
            
            display = Show(case)
            ColorBy(display, ('POINTS', 'p'))
            
            if {str(show_3d).lower()}:
                view = GetActiveView()
                if not view:
                    view = CreateRenderView()
                view.ViewSize = [800, 600]
                view.CameraPosition = [0, 0, 5]
                view.CameraFocalPoint = [0, 0, 0]
                view.CameraViewUp = [0, 1, 0]
            
            SaveScreenshot('{case_dir}/visualization.png')
            """
            
            # Write and execute script
            script_file = os.path.join(case_dir, 'visualize.py')
            with open(script_file, 'w') as f:
                f.write(script)
            
            subprocess.run(['pvpython', script_file], check=True)
            
        except Exception as e:
            print(f"Error visualizing OpenFOAM results: {str(e)}")

    def visualize_cantera_results(self, gas: ct.Solution, show_heat_release: bool = True,
                                show_species: bool = True, animate: bool = False) -> Optional[plt.Figure]:
        """Visualize Cantera simulation results"""
        try:
            self.fig = plt.figure(figsize=(12, 8))
            
            if show_heat_release and show_species:
                self.ax1 = self.fig.add_subplot(211)
                self.ax2 = self.fig.add_subplot(212)
            else:
                self.ax1 = self.fig.add_subplot(111)
            
            # Plot temperature and pressure
            self.ax1.plot(gas.T, gas.P/1e5, 'b-', label='Temperature')
            self.ax1.set_xlabel('Temperature (K)')
            self.ax1.set_ylabel('Pressure (bar)')
            self.ax1.legend()
            
            if show_heat_release and show_species:
                # Plot species mole fractions
                for species in gas.species_names:
                    self.ax2.plot(gas.T, gas[species].X, label=species)
                self.ax2.set_xlabel('Temperature (K)')
                self.ax2.set_ylabel('Mole Fraction')
                self.ax2.legend()
            
            if animate:
                self._animate_cantera_results(gas)
            
            plt.tight_layout()
            return self.fig
            
        except Exception as e:
            print(f"Error visualizing Cantera results: {str(e)}")
            return None

    def _animate_cantera_results(self, gas: ct.Solution) -> None:
        """Create animation of Cantera results"""
        try:
            def update(frame):
                self.ax1.clear()
                self.ax2.clear()
                
                # Update gas state
                gas.TP = 300 + frame * 10, 101325
                
                # Update plots
                self.ax1.plot(gas.T, gas.P/1e5, 'b-', label='Temperature')
                self.ax1.set_xlabel('Temperature (K)')
                self.ax1.set_ylabel('Pressure (bar)')
                self.ax1.legend()
                
                for species in gas.species_names:
                    self.ax2.plot(gas.T, gas[species].X, label=species)
                self.ax2.set_xlabel('Temperature (K)')
                self.ax2.set_ylabel('Mole Fraction')
                self.ax2.legend()
            
            self.animation = FuncAnimation(
                self.fig, update, frames=50,
                interval=100, blit=False
            )
            
        except Exception as e:
            print(f"Error creating animation: {str(e)}")

    def _add_streamlines(self, x: np.ndarray, y: np.ndarray, z: np.ndarray) -> None:
        """Add streamlines to the plot"""
        try:
            # Create synthetic velocity field for demonstration
            u = np.ones_like(x)
            v = np.zeros_like(y)
            w = np.zeros_like(z)
            
            self.ax.streamplot(x, y, u, v, color='b', alpha=0.5)
            
        except Exception as e:
            print(f"Error adding streamlines: {str(e)}")

    def _add_contours(self, x: np.ndarray, y: np.ndarray, z: np.ndarray) -> None:
        """Add contour lines to the plot"""
        try:
            # Create synthetic scalar field for demonstration
            field = np.sqrt(x**2 + y**2)
            
            self.ax.tricontour(x, y, field, colors='k', alpha=0.5)
            
        except Exception as e:
            print(f"Error adding contours: {str(e)}")

    def save_visualization(self, filename: str) -> None:
        """Save the current visualization to a file"""
        try:
            if self.fig:
                self.fig.savefig(filename, dpi=300, bbox_inches='tight')
            if self.animation:
                self.animation.save(filename.replace('.png', '.gif'),
                                 writer='pillow', fps=10)
        except Exception as e:
            print(f"Error saving visualization: {str(e)}")

    def create_3d_nozzle_plot(self, nozzle_geometry: Any) -> Optional[plt.Figure]:
        """Create a 3D visualization of the nozzle geometry"""
        try:
            self.fig = plt.figure(figsize=(12, 8))
            self.ax = self.fig.add_subplot(111, projection='3d')
            
            # Get nozzle contour points
            if hasattr(nozzle_geometry, 'contour_points'):
                x, y = zip(*nozzle_geometry.contour_points)
                z = np.zeros_like(x)
                
                # Create 3D surface by rotating around x-axis
                theta = np.linspace(0, 2*np.pi, 100)
                X, Theta = np.meshgrid(x, theta)
                Y = np.outer(y, np.cos(theta))
                Z = np.outer(y, np.sin(theta))
                
                self.ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
            
            self.ax.set_xlabel('X')
            self.ax.set_ylabel('Y')
            self.ax.set_zlabel('Z')
            self.ax.set_title('3D Nozzle Geometry')
            
            plt.tight_layout()
            return self.fig
            
        except Exception as e:
            print(f"Error creating 3D nozzle plot: {str(e)}")
            return None

class NozzleVisualizerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.visualizer = NozzleVisualizer()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Nozzle Analysis Visualizer')
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Create tabs for different visualizations
        self.create_mesh_tab(tabs)
        self.create_flow_tab(tabs)
        self.create_chemistry_tab(tabs)
        
    def create_mesh_tab(self, tabs):
        mesh_tab = QWidget()
        layout = QVBoxLayout(mesh_tab)
        
        # Controls
        controls = QHBoxLayout()
        self.mesh_file_btn = QPushButton('Select Mesh File')
        self.mesh_file_btn.clicked.connect(self.select_mesh_file)
        controls.addWidget(self.mesh_file_btn)
        
        self.show_streamlines = QPushButton('Show Streamlines')
        self.show_streamlines.clicked.connect(self.toggle_streamlines)
        controls.addWidget(self.show_streamlines)
        
        layout.addLayout(controls)
        
        # Canvas for mesh visualization
        self.mesh_canvas = FigureCanvas(Figure(figsize=(8, 6)))
        layout.addWidget(self.mesh_canvas)
        
        tabs.addTab(mesh_tab, "Mesh Visualization")
        
    def create_flow_tab(self, tabs):
        flow_tab = QWidget()
        layout = QVBoxLayout(flow_tab)
        
        # Controls
        controls = QHBoxLayout()
        self.flow_dir_btn = QPushButton('Select OpenFOAM Case')
        self.flow_dir_btn.clicked.connect(self.select_flow_dir)
        controls.addWidget(self.flow_dir_btn)
        
        self.show_contours = QPushButton('Toggle Contours')
        self.show_contours.clicked.connect(self.toggle_contours)
        controls.addWidget(self.show_contours)
        
        layout.addLayout(controls)
        
        # Canvas for flow visualization
        self.flow_canvas = FigureCanvas(Figure(figsize=(8, 6)))
        layout.addWidget(self.flow_canvas)
        
        tabs.addTab(flow_tab, "Flow Visualization")
        
    def create_chemistry_tab(self, tabs):
        chem_tab = QWidget()
        layout = QVBoxLayout(chem_tab)
        
        # Controls
        controls = QHBoxLayout()
        self.chem_file_btn = QPushButton('Select Cantera File')
        self.chem_file_btn.clicked.connect(self.select_chem_file)
        controls.addWidget(self.chem_file_btn)
        
        self.show_heat_release = QPushButton('Show Heat Release')
        self.show_heat_release.clicked.connect(self.toggle_heat_release)
        controls.addWidget(self.show_heat_release)
        
        layout.addLayout(controls)
        
        # Canvas for chemistry visualization
        self.chem_canvas = FigureCanvas(Figure(figsize=(8, 6)))
        layout.addWidget(self.chem_canvas)
        
        tabs.addTab(chem_tab, "Chemistry Visualization")
        
    def select_mesh_file(self):
        try:
            file_name, _ = QFileDialog.getOpenFileName(self, "Select Mesh File", "", "Gmsh Files (*.geo)")
            if file_name:
                fig = self.visualizer.visualize_gmsh_mesh(file_name)
                if fig:
                    self.mesh_canvas.figure = fig
                    self.mesh_canvas.draw()
                else:
                    QMessageBox.warning(self, "Error", "Failed to visualize mesh")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading mesh file: {str(e)}")
            
    def select_flow_dir(self):
        try:
            dir_name = QFileDialog.getExistingDirectory(self, "Select OpenFOAM Case")
            if dir_name:
                result = self.visualizer.visualize_openfoam_results(dir_name)
                if result:
                    QMessageBox.information(self, "Success", "Flow visualization completed")
                else:
                    QMessageBox.warning(self, "Error", "Failed to visualize flow")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading flow case: {str(e)}")
            
    def select_chem_file(self):
        try:
            file_name, _ = QFileDialog.getOpenFileName(self, "Select Cantera File", "", "YAML Files (*.yaml)")
            if file_name:
                gas = ct.Solution(file_name)
                fig = self.visualizer.visualize_cantera_results(gas)
                if fig:
                    self.chem_canvas.figure = fig
                    self.chem_canvas.draw()
                else:
                    QMessageBox.warning(self, "Error", "Failed to visualize chemistry")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading chemistry file: {str(e)}")
            
    def toggle_streamlines(self):
        try:
            if hasattr(self, 'current_mesh_file'):
                fig = self.visualizer.visualize_gmsh_mesh(self.current_mesh_file, show_streamlines=True)
                if fig:
                    self.mesh_canvas.figure = fig
                    self.mesh_canvas.draw()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error toggling streamlines: {str(e)}")
        
    def toggle_contours(self):
        try:
            if hasattr(self, 'current_flow_dir'):
                result = self.visualizer.visualize_openfoam_results(self.current_flow_dir, show_contours=True)
                if result:
                    QMessageBox.information(self, "Success", "Contours updated")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error toggling contours: {str(e)}")
        
    def toggle_heat_release(self):
        try:
            if hasattr(self, 'current_gas'):
                fig = self.visualizer.visualize_cantera_results(self.current_gas, show_heat_release=True)
                if fig:
                    self.chem_canvas.figure = fig
                    self.chem_canvas.draw()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error toggling heat release: {str(e)}")

def main():
    app = QApplication([])
    window = NozzleVisualizerGUI()
    window.show()
    app.exec() 