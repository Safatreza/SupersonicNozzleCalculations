# Gas Dynamics Fundamentals

## Introduction
This document provides the theoretical foundation for the gas dynamics principles used in the Supersonic Nozzle Analysis Tool. Understanding these concepts is essential for proper use and interpretation of the tool's results.

## Basic Concepts

### 1. Conservation Laws
The analysis of nozzle flows is based on three fundamental conservation laws:

1. **Conservation of Mass**
   - Continuity equation: $\dot{m} = \rho A V = \text{constant}$
   - Where:
     - $\dot{m}$ = mass flow rate
     - $\rho$ = density
     - $A$ = cross-sectional area
     - $V$ = velocity

2. **Conservation of Momentum**
   - Euler's equation for inviscid flow
   - Includes pressure and inertial forces
   - Critical for shock wave analysis

3. **Conservation of Energy**
   - First law of thermodynamics
   - Total enthalpy remains constant in adiabatic flow
   - $h_0 = h + \frac{V^2}{2} = \text{constant}$

### 2. Isentropic Flow Relations
The tool uses isentropic flow relations for basic calculations:

- **Temperature Ratio**:
  $\frac{T_0}{T} = 1 + \frac{\gamma - 1}{2}M^2$

- **Pressure Ratio**:
  $\frac{P_0}{P} = \left(1 + \frac{\gamma - 1}{2}M^2\right)^{\frac{\gamma}{\gamma-1}}$

- **Density Ratio**:
  $\frac{\rho_0}{\rho} = \left(1 + \frac{\gamma - 1}{2}M^2\right)^{\frac{1}{\gamma-1}}$

Where:
- $T_0, P_0, \rho_0$ = stagnation conditions
- $T, P, \rho$ = static conditions
- $M$ = Mach number
- $\gamma$ = specific heat ratio

### 3. Area-Mach Number Relation
The relationship between nozzle area and Mach number is crucial for design:

$\frac{A}{A^*} = \frac{1}{M}\left[\frac{2}{\gamma+1}\left(1 + \frac{\gamma-1}{2}M^2\right)\right]^{\frac{\gamma+1}{2(\gamma-1)}}$

Where:
- $A$ = local area
- $A^*$ = throat area
- $M$ = local Mach number

## Assumptions and Limitations

### 1. Isentropic Flow Assumptions
The basic calculations assume:
- Adiabatic flow (no heat transfer)
- Reversible process (no friction)
- Perfect gas behavior
- Steady flow
- One-dimensional flow

### 2. Real Flow Effects
The following effects are not accounted for in basic calculations:
- Viscous effects
- Heat transfer
- Chemical reactions
- Multi-dimensional flow
- Unsteady effects

These effects are addressed in the CFD analysis module.

## Shock Waves

### 1. Normal Shocks
- Occur when flow is forced to decelerate from supersonic to subsonic
- Governed by Rankine-Hugoniot relations
- Cause entropy increase and total pressure loss

### 2. Oblique Shocks
- Form when flow is turned through an angle
- Common in supersonic nozzles with non-uniform expansion
- Can be analyzed using shock relations

## Boundary Layer Effects

### 1. Viscous Effects
- Boundary layer growth reduces effective flow area
- Causes total pressure loss
- Affects heat transfer

### 2. Separation
- Can occur in over-expanded nozzles
- Affects thrust performance
- Important for off-design operation

## Practical Applications

### 1. Nozzle Design
- Area ratio selection based on desired exit Mach number
- Contour design to minimize losses
- Consideration of boundary layer effects

### 2. Performance Analysis
- Thrust calculation
- Flow separation prediction
- Heat transfer estimation

## References
1. Anderson, J. D. (2016). *Modern Compressible Flow: With Historical Perspective*. McGraw-Hill Education.
2. Shapiro, A. H. (1953). *The Dynamics and Thermodynamics of Compressible Fluid Flow*. John Wiley & Sons.
3. Liepmann, H. W., & Roshko, A. (1957). *Elements of Gasdynamics*. John Wiley & Sons. 