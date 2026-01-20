# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from typing import Any
from urllib import parse

from ansys.seascape.scapp import LayoutWindow


# Mock classes for rhsc classes
class SeaScapeDB(object):
    def __init__(self, db_name) -> None:
        self.db_name = db_name

    def __repr__(self) -> str:
        return f'SeaScapeDB("{self.db_name}")'


class Instance(object):
    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'Instance("{self.name}")'


class Pin(object):
    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'Pin("{self.name}")'


class Net(object):
    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'Net("{self.name}")'


class Layer(object):
    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'Layer("{self.name}")'


class View(object):
    def __init__(self, dbname, name, type) -> None:
        self.dbname = dbname
        self.name = name
        self.type = type

    def __repr__(self) -> str:
        return f'View("{self.dbname}","{self.name}", "{self.type}")'


class LayoutWindow(object):
    def __init__(self, gui_name) -> None:
        self.gui_name = gui_name

    def __repr__(self) -> str:
        return f'LayoutWindow("{self.gui_name}")'


class Launcher(object):
    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'Launcher("{self.name}")'


class OptionsBundle(dict):
    def __init__(self, opts) -> None:
        super(OptionsBundle, self).__init__(**opts)

    def __repr__(self) -> str:
        return f"OptionsBundle({super(OptionsBundle, self).__repr__()})"

    def create_from_dict(opt: dict):
        return OptionsBundle(opt)


class RHSC_Mock:
    def open_db(name: str):
        return SeaScapeDB(name)

    def give_everything():
        return [
            Instance("X16/S6"),
            Pin("VDD"),
            Net("MCNOS"),
            Layer("RLANS"),
            View("path/to/seascapedb", "uv", "UserView"),
            LayoutWindow("windowname"),
            Launcher("ll"),
        ]

    def get_options():
        return OptionsBundle({"option1": "value1", "option2": "value2", "option3": "value3"})


class CustomEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        # if isinstance(o, (SeaScapeDB, Instance, Net, Pin)):
        #     return repr(o)
        # elif isinstance(o, OptionsBundle):
        #     return repr(o)
        return repr(o)


def _json_encode(oo: Any) -> str:
    if isinstance(oo, OptionsBundle):
        ee = CustomEncoder()
        val = ee.default(oo)
        return ee.encode(val)
    # elif isinstance(oo, (list, tuple, set)):
    #     return repr(oo) # return f"{oo.__class__.__name__}(" + repr + ")"
    else:
        return json.dumps(oo, cls=CustomEncoder)


class RHSC_MockServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if self.path == "/kill":
            self.wfile.write(bytes("<html><head><title>Mock RHSC server</title></head>", "utf-8"))
            self.wfile.write(bytes("<body><p>Server Closed successfully.</p></body>", "utf-8"))
            self.wfile.write(bytes("</html>", "utf-8"))
            self.server._BaseServer__shutdown_request = True
        else:
            self.wfile.write(bytes("<html><head><title>Mock RHSC server</title></head>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        pargs = parse.parse_qs(post_data)
        cmd = pargs.get("command")[0] if pargs.get("command") else "None"
        self.log_message(f"Received command: {cmd}")
        if cmd == "None":
            out = eval(cmd)  # '"null"'
        else:
            try:
                out = eval("RHSC_Mock." + cmd)
            except Exception as ee:
                out = ee  ##################################### Fill up
        out_str = _json_encode(out)

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(out_str, "utf-8"))


if __name__ == "__main__":
    hostName = "localhost"
    serverPort = 0
    webServer = HTTPServer((hostName, serverPort), RHSC_MockServer)
    msg = f"Server started: http://{hostName}:{webServer.server_port}"
    with open("port.out", "w") as f:
        f.write(msg)
    print(msg)
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        webServer.server_close()
        print("Server stopped.")
