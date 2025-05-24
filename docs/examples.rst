Examples
========

This section provides detailed examples of using the Supersonic Nozzle Calculations package.

Basic Nozzle Analysis
-------------------

Simple Convergent-Divergent Nozzle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from supersonic_nozzle import ConvergentDivergentNozzle

    # Create nozzle
    nozzle = ConvergentDivergentNozzle(
        throat_area=0.1,
        exit_area=0.5,
        length=1.0
    )

    # Calculate properties
    area_ratio = nozzle.calculate_area_ratio()
    expansion_ratio = nozzle.calculate_expansion_ratio()

    print(f"Area ratio: {area_ratio}")
    print(f"Expansion ratio: {expansion_ratio}")

Elliptic Nozzle
~~~~~~~~~~~~~

.. code-block:: python

    from supersonic_nozzle import EllipticNozzle

    # Create elliptic nozzle
    nozzle = EllipticNozzle(
        throat_area=0.1,
        exit_area=0.5,
        length=1.0,
        num_lobes=4,
        lobe_angle=15
    )

    # Generate geometry
    points = nozzle.generate_geometry()
    print(f"Number of points: {len(points)}")

Bell Nozzle
~~~~~~~~~~

.. code-block:: python

    from supersonic_nozzle import BellNozzle

    # Create bell nozzle
    nozzle = BellNozzle(
        throat_area=0.1,
        exit_area=0.5,
        length=1.0,
        expansion_angle=15
    )

    # Calculate contour
    contour = nozzle.calculate_contour()
    print(f"Contour points: {len(contour)}")

Film Cooling Analysis
-------------------

Basic Film Cooling
~~~~~~~~~~~~~~~~

.. code-block:: python

    from supersonic_nozzle import ConvergentDivergentNozzle, FilmCooling

    # Create nozzle and cooling
    nozzle = ConvergentDivergentNozzle(
        throat_area=0.1,
        exit_area=0.5,
        length=1.0
    )

    cooling = FilmCooling(
        nozzle=nozzle,
        coolant_mass_flow=0.1,
        coolant_temperature=300
    )

    # Analyze cooling
    results = cooling.analyze()
    print(f"Cooling effectiveness: {results.effectiveness}")
    print(f"Wall temperature: {results.wall_temperature} K")

Advanced Film Cooling
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from supersonic_nozzle import FilmCooling

    # Create advanced cooling configuration
    cooling = FilmCooling(
        nozzle=nozzle,
        coolant_mass_flow=0.1,
        coolant_temperature=300,
        injection_angle=30,
        slot_height=0.001,
        turbulence_model="k-epsilon"
    )

    # Run detailed analysis
    results = cooling.analyze_detailed()
    print(f"Local effectiveness: {results.local_effectiveness}")
    print(f"Heat transfer coefficient: {results.heat_transfer_coefficient}")

CFD Analysis
----------

Basic CFD Simulation
~~~~~~~~~~~~~~~~~

.. code-block:: python

    from supersonic_nozzle import CFDIntegration

    # Set up CFD
    cfd = CFDIntegration(
        nozzle=nozzle,
        inlet_pressure=1e6,
        inlet_temperature=3000,
        turbulence_model="k-epsilon"
    )

    # Run simulation
    results = cfd.run_simulation()
    print(f"Thrust: {results.thrust} N")
    print(f"Exit Mach number: {results.exit_mach}")

Advanced CFD Analysis
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from supersonic_nozzle import CFDIntegration

    # Create advanced CFD setup
    cfd = CFDIntegration(
        nozzle=nozzle,
        inlet_pressure=1e6,
        inlet_temperature=3000,
        turbulence_model="k-omega",
        mesh_refinement=2,
        convergence_criteria=1e-6
    )

    # Run detailed simulation
    results = cfd.run_detailed_simulation()
    print(f"Flow field: {results.flow_field.shape}")
    print(f"Wall heat flux: {results.wall_heat_flux}")

Chemistry Integration
------------------

Basic Chemistry Analysis
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from supersonic_nozzle import ChemistryIntegration
    import cantera as ct

    # Set up chemistry
    gas = ct.Solution('gri30.yaml')
    chemistry = ChemistryIntegration(nozzle, gas)

    # Run analysis
    results = chemistry.analyze()
    print(f"Species concentrations: {results.species}")

Advanced Chemistry
~~~~~~~~~~~~~~~~

.. code-block:: python

    from supersonic_nozzle import ChemistryIntegration
    import cantera as ct

    # Create detailed chemistry setup
    gas = ct.Solution('gri30.yaml')
    chemistry = ChemistryIntegration(
        nozzle=nozzle,
        gas=gas,
        reaction_mechanism="gri30",
        transport_model="multicomponent"
    )

    # Run detailed analysis
    results = chemistry.analyze_detailed()
    print(f"Reaction rates: {results.reaction_rates}")
    print(f"Transport properties: {results.transport_properties}")

Visualization Examples
-------------------

Basic Visualization
~~~~~~~~~~~~~~~~

.. code-block:: python

    from supersonic_nozzle import NozzleVisualizer

    # Create visualizer
    visualizer = NozzleVisualizer(nozzle)

    # Visualize geometry
    visualizer.visualize_geometry()
    visualizer.save_visualization("geometry.png")

Advanced Visualization
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from supersonic_nozzle import NozzleVisualizer

    # Create advanced visualizer
    visualizer = NozzleVisualizer(
        nozzle=nozzle,
        style="dark",
        colormap="viridis",
        show_grid=True
    )

    # Create 3D visualization
    visualizer.visualize_3d()
    visualizer.add_streamlines()
    visualizer.add_contours()
    visualizer.save_visualization("advanced_3d.png")

Complete Workflow Example
----------------------

.. code-block:: python

    from supersonic_nozzle import (
        ConvergentDivergentNozzle,
        FilmCooling,
        CFDIntegration,
        ChemistryIntegration,
        NozzleVisualizer
    )
    import cantera as ct

    # Create nozzle
    nozzle = ConvergentDivergentNozzle(
        throat_area=0.1,
        exit_area=0.5,
        length=1.0
    )

    # Film cooling analysis
    cooling = FilmCooling(
        nozzle=nozzle,
        coolant_mass_flow=0.1,
        coolant_temperature=300
    )
    cooling_results = cooling.analyze()

    # CFD analysis
    cfd = CFDIntegration(
        nozzle=nozzle,
        inlet_pressure=1e6,
        inlet_temperature=3000
    )
    cfd_results = cfd.run_simulation()

    # Chemistry analysis
    gas = ct.Solution('gri30.yaml')
    chemistry = ChemistryIntegration(nozzle, gas)
    chemistry_results = chemistry.analyze()

    # Visualization
    visualizer = NozzleVisualizer(nozzle)
    visualizer.visualize_geometry()
    visualizer.visualize_cfd_results(cfd_results)
    visualizer.visualize_chemistry_results(chemistry_results)
    visualizer.save_visualization("complete_analysis.png") 