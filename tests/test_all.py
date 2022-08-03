from typing import Tuple
from ansys.seascape import RedhawkSC
from ansys.seascape.scapp import SeaScapeDB

def launch_server() -> Tuple[str, int]:
    import subprocess
    cmd = r"python test_utils/rhsc_mockserver.py"
    pp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with open('port.out', 'r') as f: x = f.readline()
    url = x.split('//')[-1]
    address, port = url.split(':')
    port = int(port)
    return (address, port)

def test_gp():
    address, port = launch_server()
    try:    
        gp = RedhawkSC(url=f"http://{address}:{port}/")
        db = gp.open_db('testpath')
        assert type(db) == SeaScapeDB, "Failed to open db"
        # dv = gp.create_design_view()
    finally:
        if gp:
            gp.terminate()