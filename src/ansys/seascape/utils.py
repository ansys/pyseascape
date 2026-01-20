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

import inspect
import os
import sys

_include_path_stack = list(".")  # run-dir is always includable relatively
_include_file_stack = list(["top"])


def get_script_dir():
    return _include_path_stack[-1]


def gp_dbg(lvl, *msg):
    print(*msg)


def fix_abspath(file_name):
    return os.path.abspath(os.path.expanduser(file_name))


def source_file(fn, gg, ll):
    gp_dbg(10, f"source_file {fn}")
    try:
        if not os.path.exists(fn):
            raise ValueError("File %s does not exist." % (fn))
        sss = _file_to_string(fn)
        exec(sss, gg, ll)
    except:
        print(f"ERROR sourcing file {fn}, {sys.exc_info()[0].__name__}, {sys.exc_info()[1]}")
        raise


def _file_to_string(fn):
    if not os.path.exists(fn):
        raise ValueError("File %s does not exist." % (fn))
    fff = open(fn, "r")
    return fff.read()


def _include_impl(file_name, gg=None, ll=None):
    if not os.path.isabs(os.path.expanduser(file_name)):
        rel_to_dir = get_script_dir()
        extra_help = "({!r} relative to {!r})".format(file_name, rel_to_dir)
        file_name = os.path.join(rel_to_dir, file_name)
    else:
        extra_help = ""
    file_name = fix_abspath(file_name)
    _include_file_stack.append(file_name)
    _include_path_stack.append(os.path.abspath(os.path.dirname(os.path.expanduser(file_name))))
    file_name = fix_abspath(file_name)

    stack = inspect.stack()
    for iii in range(2, len(stack)):
        current_file = fix_abspath(stack[iii][1])
        if file_name == current_file:
            raise ValueError("Recursive include: {}".format(file_name))

    try:
        source_file(file_name, gg=gg, ll=ll)
    finally:
        _include_path_stack.pop()
        _include_file_stack.pop()


def include(file_name):
    """
    Include and evaluate given script

    Parameters
    ----------
    file_name: str
        File name of the script to evaluate
    """

    # ll = inspect.stack()[1].frame.f_locals ## injecting to local
    # is useless because of locals() optimization in py3
    gg = inspect.stack()[1].frame.f_globals
    _include_impl(file_name, gg=gg, ll=gg)


def write_to_file(file_name, *args, **kwargs):
    """
    Write given args and kwargs into specified file.

    Parameters
    ----------
    file_name: str
        Name of the file to be written
    args: iterable
        zero or more parameters that will be written to file, each on new line.
    kwargs: dict
        zero or more `key = value` pairs that will be written to file, each on new line.

    """
    ff = open(file_name, "w")
    for x in args:
        ff.write(f"{x}\n")
    for x, y in kwargs.items():
        ff.write(f"{x} = {y}\n")
    ff.close()
