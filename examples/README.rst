********
Examples
********

PySeascape can be used with local installation of RedHawk-SC or with a remote RedHawk-SC with running explorer_sc web service

PySeascape offers RedHawkSC (class) frontend client to connect to the RedHawk-SC (application) backend server 

Connecting to local RedHawk-SC application
------------------------------------------

If a local RedHawk-SC application exists, RedHawkSC can launch and connect to the application provided the executable path is provided.

Example:

.. code:: python

    from ansys.seascape.redhawk import RedHawkSC

    exe_path = <path-to-redhawk_sc-executable>

    gp = RedHawkSC(executable=exe_path)

Connecting to remote RedHawk-SC application
-------------------------------------------

In case of remote RedHawk-SC application, both RedHawk-SC application and explorer_sc server must be running. RedHawkSC can connect to the application using provided url to the explorer_sc server.

Example:

.. code:: python

    from ansys.seascape.redhawk import RedHawkSC

    gp = RedHawkSC(url="http://<url-of-remote-explorer_sc-server>")


Using RedHawk-SC commands and scripts in pyseascape environment
---------------------------------------------------------------

All RedHawk-SC commands and scripts can be used in PySeascape-Python environment with minimal or no changes. All RedHawk-SC function calls must be prefixed with name of RedHawkSC object.

For example:

.. code:: python

    """ 
    It is recommended to use gp as name for RedHawkSC object as it makes the script compatible 
    with almost direct execution on native RedHawk-SC application locally as well.
    """
    gp = RedHawkSC(...)
    db = gp.open_db("<path-to-db>")

    # to call create_design_view on host  
    db.create_design_view()
