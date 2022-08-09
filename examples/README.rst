********
Examples
********

PySeascape can be used with local installation of Redhawk-SC or with a remote Redhawk-SC with running explorer_sc web service

PySeascape offers RedhawkSC (class) frontend client to connect to the Redhawk-SC (application) backend server 

Connecting to local Redhawk-SC application
------------------------------------------

If a local Redhawk-SC application exists, RedhawkSC can launch and connect to the application provided the executable path is provided.

Example:

.. code:: python

    from ansys.seascape.redhawk import RedhawkSC

    execpath = <path-to-redhawk_sc-executable>

    gp = RedhawkSC(executable=execpath)

Connecting to remote Redhawk-SC application
-------------------------------------------

In case of remote Redhawk-SC application, both Redhawk-SC application and explorer_sc server must be running. RedhawkSC can connect to the application using provided url to the explorer_sc server.

Example:

.. code:: python

    from ansys.seascape.redhawk import RedhawkSC

    url = "http://<url-of-remote-explorer_sc-server>"

    gp = RedhawkSC(url=url)

Using Redhawk-SC commands and scripts in pyseascape environment
---------------------------------------------------------------

All Redhawk-SC commands and scripts can be used in PySeascape-Python environment with minimal or no changes. All Redhawk-SC function calls must be prefixed with name of RedhawkSC object.

For example:

.. code:: python

    """ 
    It is recommended to use gp as name for RedhawkSC object as it makes the script compatible 
    with almost direct execution on native Redhawk-SC application locally as well.
    """
    gp = RedhawkSC(...)

    # to call create_design_view on host  
    gp.create_design_view()
