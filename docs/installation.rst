Installation
============

Requirements
-----------

* Python 3.8 or higher
* OpenFOAM (for CFD analysis)
* Gmsh (for mesh generation)
* Cantera (for chemistry analysis)

Basic Installation
----------------

You can install the package using pip:

.. code-block:: bash

    pip install supersonic-nozzle-calculations

Development Installation
----------------------

For development, clone the repository and install with development dependencies:

.. code-block:: bash

    git clone https://github.com/Safatreza/SupersonicNozzleCalculations.git
    cd SupersonicNozzleCalculations
    pip install -e ".[dev]"

System Dependencies
-----------------

Ubuntu/Debian
~~~~~~~~~~~~

.. code-block:: bash

    sudo apt-get update
    sudo apt-get install -y openfoam-default gmsh

Windows
~~~~~~~

1. Install OpenFOAM:
   - Download from `OpenFOAM website <https://www.openfoam.com/download>`_
   - Follow the installation instructions

2. Install Gmsh:
   - Download from `Gmsh website <http://gmsh.info/bin/Windows/>`_
   - Add to system PATH

macOS
~~~~~

Using Homebrew:

.. code-block:: bash

    brew install openfoam gmsh

Verification
-----------

To verify the installation:

.. code-block:: python

    from supersonic_nozzle import NozzleGeometry
    nozzle = NozzleGeometry()
    print(nozzle)

Troubleshooting
--------------

Common Issues
~~~~~~~~~~~~

1. OpenFOAM not found:
   - Ensure OpenFOAM is installed and in PATH
   - Source OpenFOAM environment: ``source /opt/openfoam/etc/bashrc``

2. Gmsh not found:
   - Verify Gmsh installation: ``gmsh --version``
   - Add Gmsh to system PATH

3. Cantera issues:
   - Install Cantera: ``pip install cantera``
   - Set CANTERA_DATA environment variable

Getting Help
~~~~~~~~~~~

* Check the :doc:`usage` guide
* Visit our `GitHub repository <https://github.com/Safatreza/SupersonicNozzleCalculations>`_
* Open an issue for bugs or feature requests 