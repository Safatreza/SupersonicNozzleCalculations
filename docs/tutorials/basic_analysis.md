# Basic Nozzle Analysis Tutorial

This tutorial will guide you through performing a basic analysis of a convergent-divergent nozzle using the Supersonic Nozzle Analysis Tool.

## Prerequisites
- Installed Supersonic Nozzle Analysis Tool
- Basic understanding of gas dynamics (see [Gas Dynamics Fundamentals](../theory/gas_dynamics.md))

## Step 1: Launch the Application
1. Open a terminal/command prompt
2. Navigate to the project directory
3. Run the GUI application:
   ```bash
   python gui.py
   ```

## Step 2: Configure Nozzle Geometry
1. In the "Nozzle Geometry" tab:
   - Select "Convergent-Divergent" from the nozzle type dropdown
   - Set throat area: 0.01 m²
   - Set exit area: 0.02 m²
   - Set nozzle length: 1.0 m

   These values represent a nozzle with an area ratio of 2.0, suitable for achieving supersonic flow.

## Step 3: Set Flow Conditions
1. In the "Flow Conditions" tab:
   - Set static temperature: 300 K
   - Set inlet Mach number: 0.5
   - Set exit Mach number: 2.0
   - Set total pressure: 1,000,000 Pa (10 bar)

   These conditions represent typical rocket engine operating parameters.

## Step 4: Run Analysis
1. Click the "Analyze" button
2. The tool will:
   - Calculate flow properties
   - Generate nozzle contour
   - Display results

## Step 5: Interpret Results
The results panel will show:
- Total (inlet) temperature
- Exit temperature
- Exit velocity
- Exit pressure
- Area ratio

The visualization will show:
- Nozzle contour
- Temperature distribution
- Pressure distribution
- Velocity distribution

## Understanding the Results

### 1. Flow Properties
- **Total Temperature**: Represents the temperature if the flow were brought to rest isentropically
- **Exit Temperature**: The actual temperature at the nozzle exit
- **Exit Velocity**: The flow velocity at the nozzle exit
- **Exit Pressure**: The static pressure at the nozzle exit

### 2. Performance Metrics
- **Area Ratio**: Ratio of exit area to throat area
- **Expansion Ratio**: Ratio of exit pressure to ambient pressure
- **Thrust**: Calculated based on momentum and pressure forces

## Common Issues and Solutions

### 1. Flow Separation
If you see unexpected results:
- Check if the exit pressure is much lower than ambient pressure
- Consider reducing the area ratio
- Verify the inlet conditions

### 2. Subsonic Flow
If the exit Mach number is less than 1:
- Verify the area ratio is sufficient
- Check the inlet conditions
- Ensure the total pressure is high enough

## Advanced Analysis Options

### 1. Film Cooling
To add film cooling analysis:
1. Go to the "Film Cooling" tab
2. Select coolant type
3. Configure injection parameters
4. Run analysis

### 2. CFD Analysis
For detailed flow field analysis:
1. Click "CFD Analysis" button
2. Configure mesh and solver settings
3. Run simulation
4. View detailed results

## Next Steps
- Try different nozzle geometries
- Experiment with various flow conditions
- Explore film cooling analysis
- Run CFD simulations for detailed flow field analysis

## Related Resources
- [Gas Dynamics Fundamentals](../theory/gas_dynamics.md)
- [Nozzle Design Principles](../theory/nozzle_design.md)
- [Film Cooling Tutorial](film_cooling.md)
- [CFD Simulation Tutorial](cfd_simulation.md) 