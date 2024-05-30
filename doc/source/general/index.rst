******************
PySeascape Library
******************

A pythonic remotable interface to RedHawkSC and TotemSC that allows integration with other PyAnsys and Python libraries.


How to install
--------------

Install from PyPI
^^^^^^^^^^^^^^^^^

User installation can be performed by running:

.. code:: bash

    pip install ansys-seascape

OR 

.. code:: bash

    python -m pip install ansys-seascape

Install from latest GitHub source
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fetch latest source from GitHub:

.. code:: bash

    cd <your-library-directory>
    git clone https://github.com/ansys/pyseascape.git

(Optional) Create and enable virtual environment. Please refer to official `venv`_ documentation for more help regarding virtual environment setup.

.. code:: bash
    
    # Create a virtual environment
    python -m venv .venv

    # Activate it in a POSIX system
    source .venv/bin/activate

    # Activate it in Windows CMD environment
    .venv\Scripts\activate.bat

    # Activate it in Windows Powershell
    .venv\Scripts\Activate.ps1

Install the project

.. code:: bash
    
    cd pyseascape
    pip install .

Install additional requirements (if needed):

.. code:: bash

    python -m pip install -r requirements/requirements_build.txt
    python -m pip install -r requirements/requirements_doc.txt
    python -m pip install -r requirements/requirements_tests.txt

Usage
-----

*Note: Either a local installation or remote connection to licensed RedHawk-SC is required to use the pyseascape library. \
This only offers a remotable frontend interface that can run directly in native Python on any machine.*

Launching local RedHawk-SC in backend
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    from ansys.seascape import RedHawkSC

    gp = RedHawkSC(executable=path_to_executable)

OR

.. code:: python

    from ansys import seascape

    gp = seascape.RedHawkSC(executable=path_to_executable)

Connecting to remote RedHawk-SC session
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    from ansys.seascape import RedHawkSC

    url_and_port = url_or_ip_to_redhawksc_server + ":" + port
    gp = RedHawkSC(url=url_and_port)

All RedHawk-SC global functions can be called using prefix of RedHawkSC object name. Object methods can be called as normal.

Running RedHawk-SC commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^

For example:

.. code:: python

    # If gp = RedHawkSC(...)
    db = gp.open_db(db_name)  # Returns a SeascapeDB remotable object
    db.create_design_view(...)

    # Creating RedHawk-SC objects
    inst = gp.Instance("Inst_Name")

    # RedHawk-SC modules must also be prefixed by gp
    # E.g. using voltage_impact module
    gp.voltage_impact.helpers.get_pgimpact_histograms(...)

Accessing RedHawk-SC help
-------------------------

RedHawk-SC native help function supports command based as well as keyword based help.
This help can be accessed remotely as well.

.. code:: python

    # If gp = RedHawkSC(...)

    # command based help
    gp.help(command="gp.Scatter")

    # keyword based help
    gp.help(keyword="scatter")

Known issues and limitations
----------------------------

GUI features have not yet been implemented. Hence, commands like ``open_console_window``, ``open_scheduler_window`` etc. do not work yet. Commands like ``gp.scatter_plot`` also does not work as it requires drawing GUI plots.

Documentation
-------------

Please refer to RedHawk-SC Documentation.

.. LINKS AND REFERENCES
.. _black: https://github.com/psf/black
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://github.com/PyCQA/isort
.. _PyAnsys Developer's guide: https://dev.docs.pyansys.com/
.. _pre-commit: https://pre-commit.com/
.. _pytest: https://docs.pytest.org/en/stable/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _pip: https://pypi.org/project/pip/
.. _tox: https://tox.wiki/
.. _venv: https://docs.python.org/3/library/venv.html


|
