import sys
import os
from pathlib import Path

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from visualization import NozzleVisualizer
from nozzle_geometry import (
    ConvergentDivergentNozzle,
    EllipticNozzle,
    BellNozzle
)
import cantera as ct

def create_test_mesh(filename):
    """Create a simple test mesh file"""
    with open(filename, 'w') as f:
        f.write("""
        // Test mesh for visualization
        Point(1) = {0, 0, 0, 1.0};
        Point(2) = {1, 0, 0, 1.0};
        Point(3) = {1, 1, 0, 1.0};
        Point(4) = {0, 1, 0, 1.0};
        
        Line(1) = {1, 2};
        Line(2) = {2, 3};
        Line(3) = {3, 4};
        Line(4) = {4, 1};
        
        Curve Loop(1) = {1, 2, 3, 4};
        Plane Surface(1) = {1};
        """)

def create_test_openfoam_case(case_dir):
    """Create a simple test OpenFOAM case"""
    os.makedirs(case_dir, exist_ok=True)
    # Create a simple controlDict
    with open(os.path.join(case_dir, 'controlDict'), 'w') as f:
        f.write("""
        application     rhoCentralFoam;
        startFrom       startTime;
        startTime       0;
        stopAt          endTime;
        endTime         0.1;
        deltaT          1e-6;
        writeControl    adjustableRunTime;
        writeInterval   0.01;
        """)

def main():
    # Create output directories
    output_dir = Path('output')
    mesh_dir = output_dir / 'mesh'
    cfd_dir = output_dir / 'cfd'
    vis_dir = output_dir / 'visualization'
    
    for directory in [output_dir, mesh_dir, cfd_dir, vis_dir]:
        directory.mkdir(parents=True, exist_ok=True)
    
    # Initialize visualizer
    visualizer = NozzleVisualizer()
    
    # Create test nozzle geometries
    nozzles = {
        'conventional': ConvergentDivergentNozzle(0.1, 0.2, 1.0),
        'elliptic': EllipticNozzle(0.1, 0.2, 1.0, 4, 45),
        'bell': BellNozzle(0.1, 0.2, 1.0, 15)
    }
    
    # 1. Test 3D nozzle visualization
    print("\n1. Testing 3D nozzle visualization...")
    for name, nozzle in nozzles.items():
        fig = visualizer.create_3d_nozzle_plot(nozzle)
        if fig:
            visualizer.save_visualization(str(vis_dir / f'{name}_3d.png'))
            print(f"✓ {name.capitalize()} nozzle 3D visualization saved")
    
    # 2. Test Gmsh mesh visualization
    print("\n2. Testing Gmsh mesh visualization...")
    mesh_file = mesh_dir / 'test.geo'
    create_test_mesh(mesh_file)
    
    # Test 2D visualization
    fig = visualizer.visualize_gmsh_mesh(
        str(mesh_file),
        show_streamlines=True,
        show_contours=True
    )
    if fig:
        visualizer.save_visualization(str(vis_dir / 'mesh_2d.png'))
        print("✓ 2D mesh visualization saved")
    
    # Test 3D visualization
    fig = visualizer.visualize_gmsh_mesh(
        str(mesh_file),
        show_streamlines=True,
        show_contours=True,
        view_3d=True
    )
    if fig:
        visualizer.save_visualization(str(vis_dir / 'mesh_3d.png'))
        print("✓ 3D mesh visualization saved")
    
    # 3. Test OpenFOAM visualization
    print("\n3. Testing OpenFOAM visualization...")
    case_dir = str(cfd_dir)
    create_test_openfoam_case(case_dir)
    
    try:
        # Test 2D visualization
        visualizer.visualize_openfoam_results(case_dir, show_3d=False)
        print("✓ 2D OpenFOAM visualization completed")
        
        # Test 3D visualization
        visualizer.visualize_openfoam_results(case_dir, show_3d=True)
        print("✓ 3D OpenFOAM visualization completed")
    except Exception as e:
        print(f"✗ OpenFOAM visualization failed: {str(e)}")
    
    # 4. Test Cantera visualization
    print("\n4. Testing Cantera visualization...")
    try:
        # Create a test gas object
        gas = ct.Solution('gri30.yaml')
        gas.TPX = 300, 101325, 'CH4:1, O2:2, N2:7.52'
        
        # Test static visualization
        fig = visualizer.visualize_cantera_results(
            gas,
            show_heat_release=True,
            show_species=True
        )
        if fig:
            visualizer.save_visualization(str(vis_dir / 'cantera_static.png'))
            print("✓ Static Cantera visualization saved")
        
        # Test animated visualization
        fig = visualizer.visualize_cantera_results(
            gas,
            show_heat_release=True,
            show_species=True,
            animate=True
        )
        if fig:
            visualizer.save_visualization(str(vis_dir / 'cantera_animated.gif'))
            print("✓ Animated Cantera visualization saved")
    except Exception as e:
        print(f"✗ Cantera visualization failed: {str(e)}")
    
    print("\nVisualization example completed!")
    print("Check the output/visualization directory for results.")

if __name__ == '__main__':
    main() 