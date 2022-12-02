from os.path import abspath, dirname, join
import platform
import subprocess
from sys import exc_info
import time
import traceback
from typing import Tuple

from ansys.seascape import RedHawkSC
from ansys.seascape.scapp import (
    Instance,
    Launcher,
    Layer,
    LayoutWindow,
    Net,
    OptionsBundle,
    Pin,
    SeaScapeDB,
    View,
)


def launch_server() -> Tuple[str, int, subprocess.Popen]:
    import subprocess

    srv_path = join(dirname(abspath(__file__)), "test_utils", "rhsc_mockserver.py")
    three_or_not = "" if platform.system() == "Windows" else "3"
    cmd = f"python{three_or_not} {srv_path}"
    proc_handle = subprocess.Popen(cmd, shell=True)
    time.sleep(1)
    with open("port.out", "r") as f:
        x = f.readline()
    url = x.split("//")[-1]
    address, port = url.split(":")
    port = int(port)
    return (address, port, proc_handle)


def test_all():
    address, port, proc_handle = launch_server()
    gp = None
    try:
        gp = RedHawkSC(url=f"http://{address}:{port}/")
        db = gp.open_db("testpath")
        assert type(db) == SeaScapeDB, "Failed to open db"
        opts = gp.get_options()
        assert type(opts) == OptionsBundle, "Failed to get options"
        all_objs = (
            gp.give_everything()
        )  # Special command in mockserver to return all types of objects
        print(all_objs)
        assert type(all_objs) == list and [type(x) for x in all_objs] == [
            Instance,
            Pin,
            Net,
            Layer,
            View,
            LayoutWindow,
            Launcher,
        ], "Failed to get options"
        print("ALL PASS")
    except Exception as err:
        err_type, ex, tr = exc_info()
        print(ex)
        print(traceback.print_tb(tr))
    finally:
        proc_handle.kill()


if __name__ == "__main__":
    test_all()
