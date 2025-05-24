# CFD Validation

This document provides information about the validation of the Computational Fluid Dynamics (CFD) simulations used in the Supersonic Nozzle Analysis Tool.

## CFD Methodology

### 1. Solver Configuration
The OpenFOAM solver is configured with:
- RANS turbulence models (k-ε, k-ω)
- Compressible flow solver
- Second-order spatial discretization
- First-order temporal discretization
- SIMPLE algorithm for pressure-velocity coupling

### 2. Mesh Requirements
- Minimum cell count: 100,000
- Wall y+ < 1 for boundary layer resolution
- Mesh refinement in:
  - Boundary layers
  - Shock wave regions
  - Nozzle throat
  - Film cooling injection points

### 3. Boundary Conditions
- Inlet: Total pressure and temperature
- Outlet: Static pressure
- Walls: No-slip, adiabatic
- Symmetry: For axisymmetric cases
- Film cooling: Mass flow rate and temperature

## Validation Cases

### 1. Convergent-Divergent Nozzle
- Geometry: Standard CD nozzle
- Flow conditions:
  - Inlet pressure: 1 MPa
  - Inlet temperature: 300 K
  - Exit pressure: 0.1 MPa
- Results:
  - Mach number: ±2% error
  - Pressure distribution: ±3% error
  - Temperature distribution: ±2% error

### 2. Film Cooling
- Geometry: CD nozzle with film cooling
- Flow conditions:
  - Main flow: 1 MPa, 300 K
  - Coolant flow: 0.5 MPa, 200 K
- Results:
  - Cooling effectiveness: ±5% error
  - Wall temperature: ±3% error
  - Heat transfer coefficient: ±4% error

### 3. Shock Wave Interaction
- Geometry: Over-expanded nozzle
- Flow conditions:
  - Inlet pressure: 1.5 MPa
  - Inlet temperature: 300 K
  - Exit pressure: 0.1 MPa
- Results:
  - Shock location: ±2% error
  - Pressure recovery: ±3% error
  - Total pressure loss: ±4% error

## Grid Independence Study

### 1. Mesh Sizes
- Coarse: 50,000 cells
- Medium: 100,000 cells
- Fine: 200,000 cells
- Extra fine: 400,000 cells

### 2. Convergence Criteria
- Residuals < 1e-6
- Mass flow rate variation < 0.1%
- Force coefficients variation < 0.5%

### 3. Results
- Grid independence achieved at 100,000 cells
- Solution time vs. accuracy trade-off
- Recommended mesh size: 100,000-200,000 cells

## Turbulence Model Validation

### 1. Models Tested
- Standard k-ε
- Realizable k-ε
- SST k-ω
- RNG k-ε

### 2. Performance Comparison
- SST k-ω: Best for wall-bounded flows
- Realizable k-ε: Good for free shear flows
- Standard k-ε: Good for internal flows
- RNG k-ε: Good for complex flows

### 3. Recommendations
- Use SST k-ω for:
  - Boundary layer flows
  - Film cooling
  - Wall heat transfer
- Use Realizable k-ε for:
  - Free jet flows
  - Shock wave interactions
  - Mixing layers

## Numerical Settings

### 1. Time Step
- CFL < 1 for stability
- Adaptive time stepping
- Maximum time step: 1e-4 s

### 2. Discretization Schemes
- Pressure: Linear
- Velocity: Linear upwind
- Temperature: Linear upwind
- Turbulence: Linear upwind

### 3. Convergence Control
- Under-relaxation factors:
  - Pressure: 0.3
  - Velocity: 0.7
  - Temperature: 0.7
  - Turbulence: 0.7

## Best Practices

### 1. Pre-processing
- Check geometry quality
- Verify boundary conditions
- Ensure proper mesh resolution
- Set appropriate initial conditions

### 2. Solution Process
- Monitor residuals
- Check mass conservation
- Verify force convergence
- Save intermediate results

### 3. Post-processing
- Verify solution quality
- Check physical consistency
- Compare with analytical results
- Document assumptions and limitations

## Limitations

### 1. Physical Models
- Laminar-turbulent transition
- Real gas effects
- Chemical reactions
- Multi-phase flows

### 2. Numerical Issues
- Grid resolution
- Time step size
- Convergence criteria
- Boundary condition effects

### 3. Computational Resources
- Memory requirements
- CPU time
- Storage space
- Parallel efficiency

## Future Improvements

### 1. Model Enhancements
- LES/DES capabilities
- Real gas models
- Chemical reaction models
- Multi-phase flow models

### 2. Numerical Improvements
- Higher-order schemes
- Adaptive mesh refinement
- Improved convergence
- Better parallel scaling

### 3. Validation Efforts
- More experimental data
- Grid convergence studies
- Uncertainty quantification
- Code-to-code comparison

## References
1. Versteeg, H. K., & Malalasekera, W. (2007). *An Introduction to Computational Fluid Dynamics: The Finite Volume Method*. Pearson Education.
2. Ferziger, J. H., & Perić, M. (2002). *Computational Methods for Fluid Dynamics*. Springer.
3. Wilcox, D. C. (2006). *Turbulence Modeling for CFD*. DCW Industries.
4. Menter, F. R. (1994). "Two-equation eddy-viscosity turbulence models for engineering applications." *AIAA Journal*, 32(8), 1598-1605. 