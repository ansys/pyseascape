from ansys.seascape import __version__


def test_pkg_version():
    assert __version__ == "0.3.dev0"
