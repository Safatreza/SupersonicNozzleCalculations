Usage Guide
===========

This guide covers the main features and workflows of the Supersonic Nozzle Calculations package.

Basic Usage
----------

Creating a Nozzle
~~~~~~~~~~~~~~~

.. code-block:: python

    from supersonic_nozzle import ConvergentDivergentNozzle

    # Create a conventional nozzle
    nozzle = ConvergentDivergentNozzle(
        throat_area=0.1,  # m²
        exit_area=0.5,    # m²
        length=1.0        # m
    )

    # Calculate area ratio
    area_ratio = nozzle.calculate_area_ratio()
    print(f"Area ratio: {area_ratio}")

Film Cooling Analysis
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from supersonic_nozzle import FilmCooling

    # Create film cooling configuration
    cooling = FilmCooling(
        nozzle=nozzle,
        coolant_mass_flow=0.1,  # kg/s
        coolant_temperature=300  # K
    )

    # Analyze cooling effectiveness
    effectiveness = cooling.analyze()
    print(f"Cooling effectiveness: {effectiveness}")

CFD Analysis
~~~~~~~~~~~

.. code-block:: python

    from supersonic_nozzle import CFDIntegration

    # Set up CFD analysis
    cfd = CFDIntegration(
        nozzle=nozzle,
        inlet_pressure=1e6,  # Pa
        inlet_temperature=3000  # K
    )

    # Run simulation
    results = cfd.run_simulation()
    print(f"Thrust: {results.thrust} N")

Visualization
~~~~~~~~~~~~

.. code-block:: python

    from supersonic_nozzle import NozzleVisualizer

    # Create visualizer
    visualizer = NozzleVisualizer(nozzle)

    # Visualize geometry
    visualizer.visualize_geometry()
    visualizer.save_visualization("nozzle_geometry.png")

    # Visualize CFD results
    visualizer.visualize_cfd_results(results)
    visualizer.save_visualization("cfd_results.png")

Advanced Features
---------------

Chemistry Integration
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from supersonic_nozzle import ChemistryIntegration
    import cantera as ct

    # Set up chemistry
    gas = ct.Solution('gri30.yaml')
    chemistry = ChemistryIntegration(nozzle, gas)

    # Run chemistry analysis
    results = chemistry.analyze()
    print(f"Species concentrations: {results.species}")

Mesh Generation
~~~~~~~~~~~~~

.. code-block:: python

    from supersonic_nozzle import MeshGenerator

    # Create mesh generator
    mesh_gen = MeshGenerator(nozzle)

    # Generate mesh
    mesh = mesh_gen.generate(
        element_size=0.01,  # m
        refinement_level=2
    )

    # Save mesh
    mesh.save("nozzle_mesh.msh")

Command Line Interface
--------------------

The package provides a command-line interface for quick analysis:

.. code-block:: bash

    # Run basic analysis
    python -m supersonic_nozzle analyze --throat 0.1 --exit 0.5 --length 1.0

    # Run with film cooling
    python -m supersonic_nozzle analyze --cooling --coolant-flow 0.1

    # Run CFD simulation
    python -m supersonic_nozzle cfd --inlet-pressure 1e6 --inlet-temp 3000

GUI Interface
------------

For interactive use, launch the GUI:

.. code-block:: bash

    python -m supersonic_nozzle gui

The GUI provides:
* Interactive nozzle design
* Real-time visualization
* Parameter optimization
* Results export

Configuration Files
-----------------

The package uses YAML configuration files for complex setups:

.. code-block:: yaml

    # config.yaml
    nozzle:
      type: convergent-divergent
      throat_area: 0.1
      exit_area: 0.5
      length: 1.0

    cooling:
      enabled: true
      coolant_mass_flow: 0.1
      coolant_temperature: 300

    cfd:
      inlet_pressure: 1e6
      inlet_temperature: 3000
      turbulence_model: k-epsilon

Load configuration:

.. code-block:: python

    from supersonic_nozzle import load_config
    config = load_config("config.yaml")
    nozzle = config.create_nozzle() 