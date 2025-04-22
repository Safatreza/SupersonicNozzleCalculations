from inlet_temperature import calc_total_temperature
from exit_temperature import calc_static_exit_temperature
from exit_velocity import calc_exit_velocity
from pressure_ratio import calc_pressure_ratio
from thrust import calc_thrust

def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("❌ Invalid number, try again.")

if __name__ == "__main__":
    print("🚀 Supersonic Nozzle Calculations\n")

    T_static = get_float("Static temperature (K): ")
    M_inlet = get_float("Inlet Mach number: ")
    M_exit = get_float("Exit Mach number: ")
    gamma = get_float("Specific heat ratio γ (default 1.4): ") or 1.4
    cp = get_float("Specific heat at constant pressure cp (J/kg·K, default 1005): ") or 1005
    P_total = get_float("Total (stagnation) pressure (Pa): ")
    P_atm = get_float("Atmospheric pressure (Pa): ")
    mass_flow_rate = get_float("Mass flow rate (kg/s): ")
    A_exit = get_float("Exit area (m²): ")

    T0 = calc_total_temperature(T_static, M_inlet, gamma)
    Te = calc_static_exit_temperature(T0, M_exit, gamma)
    Ve = calc_exit_velocity(cp, T0, Te)
    Pe = calc_pressure_ratio(M_exit, gamma) * P_total
    thrust = calc_thrust(mass_flow_rate, Ve, Pe, P_atm, A_exit)

    print("\n📊 Results:")
    print(f"Total (Inlet) Temperature: {T0:.2f} K")
    print(f"Exit Temperature: {Te:.2f} K")
    print(f"Exit Velocity: {Ve:.2f} m/s")
    print(f"Exit Pressure: {Pe:.2f} Pa")
    print(f"Thrust: {thrust:.2f} N")
