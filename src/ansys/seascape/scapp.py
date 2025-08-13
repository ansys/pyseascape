# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

import atexit
import json
import re

import requests


class GpObject(object):
    def __init__(self, type, data):
        self.type_ = type
        self.data_ = data

    def __repr__(self):
        return f"{self.type_}({self.data_!r})"


class Instance(GpObject):
    """
    Provides remotable proxy to Instance class in RedHawk-SC.
    """

    def __init__(self, data):
        super(Instance, self).__init__("Instance", data)


class Pin(GpObject):
    """
    Provides remotable proxy to Pin class in RedHawk-SC.
    """

    def __init__(self, data):
        super(Pin, self).__init__("Pin", data)


class Net(GpObject):
    """
    Provides remotable proxy to Net class in RedHawk-SC.
    """

    def __init__(self, data):
        super(Net, self).__init__("Net", data)


class Layer(GpObject):
    """
    Provides remotable proxy to Layer class in RedHawk-SC.
    """

    def __init__(self, data):
        super(Layer, self).__init__("Layer", data)


# Remotable classes are those that have remotable APIs on the server side
class Remotable(object):
    def __init__(self, manager, identifier):
        self.manager_ = manager
        self.identifier_ = identifier

    def __repr__(self):
        return self.identifier_

    def __getattr__(self, cmd):
        return RemoteCaller(self.manager_, f"{self.identifier_}.{cmd}")


class View(Remotable):
    """
    Provides remotable proxy to all View type classes in RedHawk-SC.
    """

    def __init__(self, manager, db_name, view_name, view_type):
        self.view_type_ = view_type
        super(View, self).__init__(manager, f'SeaScapeDB("{db_name}").get("{view_name}")')


class SeaScapeDB(Remotable):
    """
    Provides remotable proxy to SeascapeDB class in RedHawk-SC.
    """

    def __init__(self, manager, db_name):
        super(SeaScapeDB, self).__init__(manager, f'SeaScapeDB("{db_name}")')


class LayoutWindow(Remotable):
    """
    Provides handler to LayoutWindow in RedHawk-SC.
    """

    def __init__(self, manager, gui_name):
        super(LayoutWindow, self).__init__(manager, f'LayoutWindow.get_handler("{gui_name}")')


class Launcher(Remotable):
    """
    Provides remotable proxy to job launcher in RedHawk-SC.
    """

    def __init__(self, manager, launcher_name):
        super(Launcher, self).__init__(manager, f'gp.LauncherRep.find_launcher("{launcher_name}")')


class XTExtractTweaks(object):
    # defined as a hack to get around the extractor options problem
    def __init__(self, *vals):
        self.vals_ = vals

    def __repr__(self):
        return f"XTExtractTweaks(*{self.vals_})"


class OptionsBase(dict):
    def __init__(self, opts):
        super(OptionsBase, self).__init__(**opts)

    def __setattr__(self, key, val):
        self[key] = val

    def __getattr__(self, key):
        return self[key]


class OptionsBundle(dict):
    """
    Provides pythonic representation to options passed to most views during their creation.
    """

    def __init__(self, opts):
        super(OptionsBundle, self).__init__(**opts)

    def __getitem__(self, key):
        if key not in self.keys():
            self[key] = OptionsBase({})
        val = self.get(key)
        return val

    def __repr__(self):
        self_repr = super(OptionsBundle, self).__repr__()
        return f"gp.OptionsBundle.create_from_dict({self_repr})"


class ModuleStoredCall(object):
    def __init__(self, mod, cmd):
        self.mod_ = mod
        self.cmd_ = cmd
        self.args_ = ""

    def __call__(self, *args, **kvargs):
        self.args_ = f"(*{args}, **{kvargs})"
        return self

    def __repr__(self):
        return f"{self.mod_}.{self.cmd_}{self.args_}"


class SCAppModule(object):
    """Supports util function calls that are passed into view creation."""

    def __init__(self, name, manager):
        self.name_ = name
        self.manager_ = manager

    def __getattr__(self, cmd):
        if cmd.endswith("_func"):
            return ModuleStoredCall(self.name_, cmd)
        else:
            return RemoteCaller(self.manager_, f"{self.name_}.{cmd}")


class SCApp(object):
    def __init__(self, url=None, executable=None, executable_work_dir="gp_rr", debug_remote=False):
        self.product_name_ = self.__class__.__name__
        self.rh_process_ = None
        if url == None and executable == None:
            raise ValueError("Either RedHawk-SC server URL or executable path must be specified.")
        if url is not None:
            self.url_ = url
            self.check_connection()
            return

        import subprocess

        remote_args = ""
        if debug_remote:
            remote_args += "debug=True,"
        remote_args = "record_commands=True,"
        pp = subprocess.Popen(
            [
                f"{executable}",
                "--message_converter",
                "off",
                "--work_dir",
                executable_work_dir,
                "-c",
                f"explorer_sc.run_communicator({remote_args})",
            ],
            stdout=subprocess.PIPE,
        )
        self.rh_process_ = pp
        subprocesses.append(self)
        for line in pp.stdout:
            line = line.decode("utf-8")
            mm = re.search("Work Directory", line)
            if mm is not None:
                print(f"{self.product_name_} {line.strip()}")
                continue
            mm = re.search("Started service: (.*)\.", line)
            if mm is None:
                continue
            self.url_ = f"http://{mm.group(1)}"
            self.check_connection()
            self.startup()
            return

    def startup(self):
        self.send_cmd("import functools", has_return=False)

    def check_connection(self):
        self.send_cmd("None")

    def send_cmd(self, cmd, has_return=True):
        try:
            d = requests.post(
                self.url_, data={"command": cmd, "return": has_return, "delayed": False}
            )
            if d.status_code == 666:
                raise ValueError(f"Reply from {self.product_name_}: {d.text} for command {cmd}")
        except requests.exceptions.ConnectionError:
            raise ValueError(f"Connection to {self.url_} not successful") from None
        return json.loads(d.text, cls=MyDecoder, manager=self)

    def terminate(self, local_only=False):
        if self.rh_process_ is None and local_only:
            return
        try:
            requests.get(f"{self.url_}/kill")
        except requests.exceptions.ConnectionError:
            # rhsc side needs to be fixed so that we don't get this exception
            pass
        self.url_ = None

    def __getattr__(self, cmd):
        return RemoteCaller(self, f"{cmd}")

    def inject_global_commands(self):
        _inject_global_commands(self)

    def write_remote_tmp_file(self, data):
        return self.send_cmd(f"gp.write_remote_tmp_file({data!r})")

    def help(self, command="", keyword=""):
        if command and keyword:
            ValueError("Only one of command or keyword can be specified.")
        if command:
            return self.send_cmd(f"help({command})")
        else:
            return self.send_cmd(f"help('{keyword}')")


class ObjConverter(object):
    """hierarchical json converter to objects like Instance, Pin, ...
    Works for dict, list, ... recursively"""

    def __init__(self, manager):
        self.manager_ = manager

    def convert(self, obj):
        if isinstance(obj, str):
            return self._convert_func(obj)
        elif isinstance(obj, (list, tuple, set)):
            return self._convert_simple_collection(obj)
        elif isinstance(obj, dict):
            return self._convert_dict(obj)
        return obj

    def _convert_simple_collection(self, obj):
        if not isinstance(obj, (list, tuple, set)):
            return obj
        new_obj = list()
        modified = False
        for item in obj:
            new_item = self.convert(item)
            new_obj.append(new_item)
            if id(new_item) != id(item):
                modified = True
        if modified:
            return type(obj)(new_obj)
        return obj

    def _convert_dict(self, obj):
        if not isinstance(obj, dict):
            return obj
        modified = False
        new_obj = type(obj)()
        for key, val in obj.items():
            new_key = self.convert(key)
            new_val = self.convert(val)
            if id(new_key) != id(key) or id(new_val) != id(val):
                modified = True
            new_obj[new_key] = new_val
        if modified:
            return new_obj
        return obj

    def _convert_func(self, ss):
        for cls_name in [
            "View",
            "SeaScapeDB",
            "LayoutWindow",
            "Launcher",
        ]:  ## these are Remotable
            if ss.startswith(cls_name):
                mm = re.match(f"{cls_name}\((.*)\)", ss)
                args = eval(mm.group(1))
                if not isinstance(args, tuple):
                    args = (args,)
                cls = globals()[cls_name]
                return cls(self.manager_, *args)
        for cls_name in ["Instance", "Pin", "Net", "Layer", "OptionsBundle"]:
            if ss.startswith(cls_name):
                return eval(ss)
        if ss.startswith("RawBytes "):
            ss = ss[len("RawBytes ") :]
            from base64 import b64decode

            return b64decode(ss)
        return ss


class MyDecoder(json.JSONDecoder):
    def __init__(self, manager):
        self.converter_ = ObjConverter(manager)
        super(MyDecoder, self).__init__()

    def decode(self, ss):
        ss = super(MyDecoder, self).decode(ss)
        return self.converter_.convert(ss)


class RemoteCaller(object):
    def __init__(self, manager, obj_attr):
        self.manager_ = manager
        self.obj_attr_ = obj_attr

    def __call__(self, *args, **kvargs):
        return self.manager_.send_cmd(f"{self.obj_attr_}(*{args}, **{kvargs})")


def _inject_global_commands(rh):
    """This is a utility function to define commonly used symbols in existing scripts
    For example, without this, it is mandatory to write gp.open_db instead of just open_db"""
    import inspect

    f_globals = inspect.stack()[2].frame.f_globals  ## caller's stack frame
    m_globals = inspect.stack()[0].frame.f_globals  ## this stack frame

    global_symbols = ["include", "write_to_file"]
    for cc in global_symbols:
        f_globals[cc] = m_globals[cc]

    if rh is None:
        return

    appsc_modules = [
        "package",
        "bqm_current",
        "deco",
    ]  # TODO: add more here for commmonly used appsc modules
    for cc in appsc_modules:
        f_globals[cc] = SCAppModule(cc, rh)

    rh_symbols = [
        "open_db",
        "open_scheduler_window",
        "create_grid_launcher",
        "create_local_launcher",
        "register_default_launcher",
        "get_default_options",
    ]
    for cc in rh_symbols:
        f_globals[cc] = getattr(rh, cc)


subprocesses = []


def cleanup():
    for pp in subprocesses:
        pp.terminate(local_only=True)


atexit.register(cleanup)
