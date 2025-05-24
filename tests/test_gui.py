import unittest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt
from visualization import NozzleVisualizerGUI
import sys

class TestNozzleVisualizerGUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)
        
    def setUp(self):
        self.window = NozzleVisualizerGUI()
        
    def test_window_title(self):
        self.assertEqual(self.window.windowTitle(), 'Nozzle Analysis Visualizer')
        
    def test_tab_widget(self):
        # Check if all tabs are present
        tabs = self.window.findChild(QTabWidget)
        self.assertIsNotNone(tabs)
        self.assertEqual(tabs.count(), 3)
        self.assertEqual(tabs.tabText(0), "Mesh Visualization")
        self.assertEqual(tabs.tabText(1), "Flow Visualization")
        self.assertEqual(tabs.tabText(2), "Chemistry Visualization")
        
    def test_mesh_tab_controls(self):
        # Check mesh tab controls
        mesh_file_btn = self.window.mesh_file_btn
        self.assertIsNotNone(mesh_file_btn)
        self.assertEqual(mesh_file_btn.text(), 'Select Mesh File')
        
        show_streamlines = self.window.show_streamlines
        self.assertIsNotNone(show_streamlines)
        self.assertEqual(show_streamlines.text(), 'Show Streamlines')
        
    def test_flow_tab_controls(self):
        # Check flow tab controls
        flow_dir_btn = self.window.flow_dir_btn
        self.assertIsNotNone(flow_dir_btn)
        self.assertEqual(flow_dir_btn.text(), 'Select OpenFOAM Case')
        
        show_contours = self.window.show_contours
        self.assertIsNotNone(show_contours)
        self.assertEqual(show_contours.text(), 'Toggle Contours')
        
    def test_chemistry_tab_controls(self):
        # Check chemistry tab controls
        chem_file_btn = self.window.chem_file_btn
        self.assertIsNotNone(chem_file_btn)
        self.assertEqual(chem_file_btn.text(), 'Select Cantera File')
        
        show_heat_release = self.window.show_heat_release
        self.assertIsNotNone(show_heat_release)
        self.assertEqual(show_heat_release.text(), 'Show Heat Release')
        
    def test_canvas_creation(self):
        # Check if canvases are created
        self.assertIsNotNone(self.window.mesh_canvas)
        self.assertIsNotNone(self.window.flow_canvas)
        self.assertIsNotNone(self.window.chem_canvas)
        
    def test_button_clicks(self):
        # Test button clicks
        QTest.mouseClick(self.window.mesh_file_btn, Qt.MouseButton.LeftButton)
        QTest.mouseClick(self.window.flow_dir_btn, Qt.MouseButton.LeftButton)
        QTest.mouseClick(self.window.chem_file_btn, Qt.MouseButton.LeftButton)
        
    @classmethod
    def tearDownClass(cls):
        cls.app.quit()

if __name__ == '__main__':
    unittest.main() 