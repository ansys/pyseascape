from typing import Tuple
from ansys.seascape import RedhawkSC
from ansys.seascape.scapp import SeaScapeDB
from os.path import abspath
from test_utils import rhsc_mockserver

def launch_server() -> Tuple[str, int]:
    import subprocess
    cmd = f"python {abspath(rhsc_mockserver.__file__)}"
    pp = subprocess.Popen(cmd, shell=True)
    with open('port.out', 'r') as f: x = f.readline()
    url = x.split('//')[-1]
    address, port = url.split(':')
    port = int(port)
    return (address, port)

def test_gp():
    address, port = launch_server()
    gp = None
    try:    
        gp = RedhawkSC(url=f"http://{address}:{port}/")
        db = gp.open_db('testpath')
        assert type(db) == SeaScapeDB, "Failed to open db"
    finally:
        if gp:
            gp.terminate()