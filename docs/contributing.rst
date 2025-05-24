Contributing
===========

We welcome contributions to the Supersonic Nozzle Calculations project! This guide will help you get started.

Development Setup
---------------

1. Fork the repository
2. Clone your fork:
   .. code-block:: bash

       git clone https://github.com/YOUR_USERNAME/SupersonicNozzleCalculations.git
       cd SupersonicNozzleCalculations

3. Install development dependencies:
   .. code-block:: bash

       pip install -e ".[dev]"

4. Set up pre-commit hooks:
   .. code-block:: bash

       pre-commit install

Coding Standards
--------------

* Follow PEP 8 style guide
* Use type hints
* Write docstrings in Google style
* Keep functions focused and small
* Write tests for new features

Testing
-------

Run tests:
.. code-block:: bash

    pytest

Run with coverage:
.. code-block:: bash

    pytest --cov=supersonic_nozzle

Run specific test file:
.. code-block:: bash

    pytest tests/test_specific.py

Documentation
-----------

Build documentation:
.. code-block:: bash

    cd docs
    make html

View documentation:
.. code-block:: bash

    python -m http.server -d _build/html

Pull Request Process
-----------------

1. Create a new branch:
   .. code-block:: bash

       git checkout -b feature/your-feature-name

2. Make your changes
3. Run tests and linting:
   .. code-block:: bash

       pytest
       black .
       isort .
       flake8
       mypy .

4. Commit your changes:
   .. code-block:: bash

       git commit -m "Add feature: your feature description"

5. Push to your fork:
   .. code-block:: bash

       git push origin feature/your-feature-name

6. Create a pull request

Code Review
---------

* All PRs require at least one review
* CI must pass
* Documentation must be updated
* Tests must be added
* Code must be formatted

Development Workflow
-----------------

1. Create issue for new feature/bug
2. Create branch from main
3. Make changes
4. Run tests and linting
5. Update documentation
6. Create PR
7. Address review comments
8. Merge after approval

Release Process
------------

1. Update version in pyproject.toml
2. Update CHANGELOG.md
3. Create release branch
4. Run full test suite
5. Build documentation
6. Create GitHub release
7. Deploy to PyPI

Getting Help
----------

* Check existing issues
* Join our community chat
* Contact maintainers

Thank you for contributing! 