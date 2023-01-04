.. _contributing_seascape:

==========
Contribute
==========
Overall guidance on contributing to a PyAnsys repository appears in
`Contribute <https://dev.docs.pyansys.com/how-to/contributing.html>`_
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar
with this guide, paying particular attention to `Guidelines and Best Practices
<https://dev.docs.pyansys.com/how-to/index.html>`_, before attempting
to contribute to PySeascape.
 
The following contribution information is specific to PySeascape.

Clone the repository
--------------------
To clone and install the latest version of PySeascape in
development mode, run:

.. code::

    git clone https://github.com/pyansys/pyseascape
    cd pyseascape
    python -m pip install --upgrade pip
    pip install -e .

Post issues
-----------
Use the `PySeascape Issues <https://github.com/pyansys/pyseascape/issues>`_
page to submit questions, report bugs, and request new features.

To reach the support team, email `pyansys.support@ansys.com <pyansys.support@ansys.com>`_.

View PySeascape documentation
-----------------------------
Documentation for the latest stable release of PySeascape is hosted at
`PySeascape Documentation <https://seascape.docs.pyansys.com>`_.  

Documentation for the latest development version, which tracks the
``main`` branch, is hosted at  `Development PySeascape Documentation <https://seascape.docs.pyansys.com/dev/>`_.
This version is automatically kept up to date via GitHub actions.

Adhere to code style
--------------------
PySeascape is compliant with `PyAnsys code style
<https://dev.docs.pyansys.com/coding_style/index.html>`_. It uses the tool
`pre-commit <https://pre-commit.com/>`_ to check the code style. You can install
and activate this tool with:

.. code:: bash

  pip install pre-commit
  pre-commit run --all-files

You can also install this as a pre-commit hook with:

.. code:: bash

  pre-commit install

This way, it's not possible for you to push code that fails the style checks.
For example::

  $ pre-commit install
  $ git commit -am "Add my cool feature."
  black....................................................................Passed
  blacken-docs.............................................................Passed
  isort....................................................................Passed
  flake8...................................................................Passed
  codespell................................................................Passed
  check for merge conflicts................................................Passed
  debug statements (python)................................................Passed
  Validate GitHub Workflows................................................Passed
