from inlet_temperature import calc_total_temperature
from exit_temperature import calc_static_exit_temperature
from exit_velocity import calc_exit_velocity
from pressure_ratio import calc_pressure_ratio
from thrust import calc_thrust
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
from visualization import NozzleVisualizer
import sys
import os
from pathlib import Path

def get_float(prompt, default=None):
    while True:
        try:
            value = input(prompt)
            if not value and default is not None:
                return default
            return float(value)
        except ValueError:
            print("❌ Invalid number, try again.")

def get_int(prompt, default=None):
    while True:
        try:
            value = input(prompt)
            if not value and default is not None:
                return default
            return int(value)
        except ValueError:
            print("❌ Invalid number, try again.")

def create_nozzle():
    print("\nSelect nozzle type:")
    print("1. Convergent-Divergent (Conventional)")
    print("2. Elliptic (with lobes)")
    print("3. Bell-shaped")
    
    choice = get_int("Enter choice (1-3): ")
    
    throat_area = get_float("Throat area (m²): ")
    exit_area = get_float("Exit area (m²): ")
    length = get_float("Nozzle length (m): ")
    
    try:
        if choice == 1:
            return ConvergentDivergentNozzle(throat_area, exit_area, length)
        elif choice == 2:
            num_lobes = get_int("Number of lobes (default 4): ", 4)
            lobe_angle = get_float("Lobe angle in degrees (default 45): ", 45)
            return EllipticNozzle(throat_area, exit_area, length, num_lobes, lobe_angle)
        elif choice == 3:
            wall_angle = get_float("Wall angle in degrees (default 15): ", 15)
            return BellNozzle(throat_area, exit_area, length, wall_angle)
        else:
            print("Invalid choice, defaulting to conventional nozzle")
            return ConvergentDivergentNozzle(throat_area, exit_area, length)
    except Exception as e:
        print(f"Error creating nozzle: {str(e)}")
        sys.exit(1)

def get_cooling_config():
    print("\nFilm Cooling Configuration:")
    print("1. Air")
    print("2. Helium")
    print("3. Neon")
    
    coolant_choice = get_int("Select coolant type (1-3): ")
    coolant_type = {
        1: CoolantType.AIR,
        2: CoolantType.HELIUM,
        3: CoolantType.NEON
    }.get(coolant_choice, CoolantType.AIR)
    
    try:
        angle = get_float("Injection angle from wall (degrees): ")
        slot_height = get_float("Slot height (m): ")
        slot_width = get_float("Slot width (m): ")
        blowing_ratio = get_float("Blowing ratio: ")
        coolant_temp = get_float("Coolant temperature (K): ")
        coolant_velocity = get_float("Coolant injection velocity (m/s): ")
        
        return InjectionConfig(
            angle=angle,
            slot_height=slot_height,
            slot_width=slot_width,
            blowing_ratio=blowing_ratio,
            coolant_type=coolant_type,
            coolant_temp=coolant_temp,
            coolant_velocity=coolant_velocity
        )
    except Exception as e:
        print(f"Error creating cooling configuration: {str(e)}")
        sys.exit(1)

def get_cfd_config():
    print("\nCFD Configuration:")
    try:
        mesh_resolution = get_int("Mesh resolution (default 100): ", 100)
        print("\nTurbulence Model:")
        print("1. k-epsilon")
        print("2. k-omega SST")
        model_choice = get_int("Select model (1-2): ")
        turbulence_model = "kEpsilon" if model_choice == 1 else "kOmegaSST"
        
        print("\nWall Treatment:")
        print("1. Wall Functions")
        print("2. Low Reynolds")
        wall_choice = get_int("Select treatment (1-2): ")
        wall_treatment = "wallFunction" if wall_choice == 1 else "lowRe"
        
        max_iterations = get_int("Maximum iterations (default 1000): ", 1000)
        convergence = get_float("Convergence criteria (default 1e-6): ", 1e-6)
        time_step = get_float("Time step (default 1e-6): ", 1e-6)
        end_time = get_float("End time (default 0.1): ", 0.1)
        
        return create_cfd_config(
            mesh_resolution=mesh_resolution,
            turbulence_model=turbulence_model,
            wall_treatment=wall_treatment,
            max_iterations=max_iterations,
            convergence_criteria=convergence,
            time_step=time_step,
            end_time=end_time
        )
    except Exception as e:
        print(f"Error creating CFD configuration: {str(e)}")
        sys.exit(1)

def setup_output_directories():
    """Create necessary output directories"""
    directories = ['output', 'output/mesh', 'output/cfd', 'output/visualization']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def main():
    try:
        print("🚀 Supersonic Nozzle Calculations\n")
        
        # Setup output directories
        setup_output_directories()
        
        # Initialize visualizer
        visualizer = NozzleVisualizer()

        # Get nozzle geometry
        nozzle = create_nozzle()
        
        # Get flow parameters
        T_static = get_float("Static temperature (K): ")
        M_inlet = get_float("Inlet Mach number: ")
        M_exit = get_float("Exit Mach number: ")
        gamma = get_float("Specific heat ratio γ (default 1.4): ", 1.4)
        cp = get_float("Specific heat at constant pressure cp (J/kg·K, default 1005): ", 1005)
        P_total = get_float("Total (stagnation) pressure (Pa): ")
        P_atm = get_float("Atmospheric pressure (Pa): ")
        mass_flow_rate = get_float("Mass flow rate (kg/s): ")

        # Calculate nozzle parameters
        area_ratio = calculate_area_ratio(nozzle)
        required_expansion = calculate_expansion_ratio(nozzle, gamma, M_exit)
        
        # Calculate flow parameters
        T0 = calc_total_temperature(T_static, M_inlet, gamma)
        Te = calc_static_exit_temperature(T0, M_exit, gamma)
        Ve = calc_exit_velocity(cp, T0, Te)
        Pe = calc_pressure_ratio(M_exit, gamma) * P_total
        thrust = calc_thrust(mass_flow_rate, Ve, Pe, P_atm, nozzle.exit_area)

        # Store analytical results for validation
        analytical_results = {
            'exit_temperature': Te,
            'exit_velocity': Ve,
            'exit_pressure': Pe,
            'thrust': thrust
        }

        # Film cooling analysis
        print("\nWould you like to perform film cooling analysis? (y/n)")
        if input().lower() == 'y':
            cooling_config = get_cooling_config()
            
            # Generate points for analysis (every 10% of nozzle length)
            x_points = [nozzle.length * i / 10 for i in range(11)]
            
            # Perform cooling analysis
            cooling_results = analyze_cooling_performance(
                cooling_config,
                x_points,
                Te,  # Using exit temperature as mainstream temperature
                Ve   # Using exit velocity as mainstream velocity
            )
            
            print("\n📊 Film Cooling Results:")
            print(f"Coolant Type: {cooling_config.coolant_type.value}")
            print("\nDistance from Injection | Effectiveness | Wall Temperature | Heat Transfer Coef.")
            print("-" * 80)
            
            for i, x in enumerate(x_points):
                print(f"{x:8.3f} m | {cooling_results['effectiveness'][i]:12.3f} | "
                      f"{cooling_results['wall_temperature'][i]:14.1f} K | "
                      f"{cooling_results['heat_transfer_coefficient'][i]:16.1f} W/m²·K")

        # CFD analysis
        print("\nWould you like to perform CFD analysis? (y/n)")
        if input().lower() == 'y':
            cfd_config = get_cfd_config()
            
            # Create flow conditions dictionary
            flow_conditions = {
                'inlet_temperature': T0,
                'inlet_pressure': P_total,
                'inlet_mach': M_inlet,
                'exit_pressure': P_atm,
                'gamma': gamma
            }
            
            # Initialize and run CFD
            cfd = OpenFOAMIntegration()
            print("\nSetting up CFD case...")
            cfd.setup_case(nozzle, flow_conditions, cfd_config)
            
            print("\nRunning CFD simulation...")
            cfd.run_simulation()
            
            print("\nAnalyzing results...")
            validation = cfd.validate_with_analytical(analytical_results)
            
            print("\n📊 CFD Validation Results:")
            print("\nParameter | Relative Error | Absolute Error")
            print("-" * 50)
            for param, errors in validation.items():
                print(f"{param:10} | {errors['relative_error']:14.2%} | {errors['absolute_error']:14.2e}")

        # Visualization
        print("\nWould you like to visualize the results? (y/n)")
        if input().lower() == 'y':
            # Visualize mesh
            mesh_file = 'output/mesh/nozzle.geo'
            if os.path.exists(mesh_file):
                fig = visualizer.visualize_gmsh_mesh(mesh_file)
                if fig:
                    visualizer.save_visualization('output/visualization/mesh.png')
            
            # Visualize CFD results
            cfd_dir = 'output/cfd'
            if os.path.exists(cfd_dir):
                visualizer.visualize_openfoam_results(cfd_dir)
            
            # Visualize chemistry results if available
            chem_file = 'output/chemistry/results.yaml'
            if os.path.exists(chem_file):
                import cantera as ct
                gas = ct.Solution(chem_file)
                fig = visualizer.visualize_cantera_results(gas)
                if fig:
                    visualizer.save_visualization('output/visualization/chemistry.png')

        print("\n📊 Nozzle Performance Results:")
        print(f"Nozzle Type: {nozzle.__class__.__name__}")
        print(f"Area Ratio: {area_ratio:.2f}")
        print(f"Required Expansion Ratio: {required_expansion:.2f}")
        print(f"Total (Inlet) Temperature: {T0:.2f} K")
        print(f"Exit Temperature: {Te:.2f} K")
        print(f"Exit Velocity: {Ve:.2f} m/s")
        print(f"Exit Pressure: {Pe:.2f} Pa")
        print(f"Thrust: {thrust:.2f} N")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
