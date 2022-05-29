
# VC FS

import os
import time

from vc_base import vc_base

from Entry import Entry
from State import State

import Utils

class vc_fs(vc_base):

    def __init__(self, root, state, logger):
        self.name = "FS"
        super().__init__(root, state, logger)
        self.info = None
        # regular expression objects to ignore
        self.ignore_reos = None

    def get_info(self):
        """ When this is called, self.display may be None """
        if self.info is not None:
            return

        D = os.getcwd()
        D = D.replace(os.getenv("HOME"), "~")
        self.info = D

    def status(self, ignores):
        result = [ "NULL" ]

        L = os.listdir()

        glob_reo = self.state.glob_compile()
        self.compile_reos()
        for name in L:
            if ignores and self.ignored(name):
                continue
            if not self.state.glob_match(glob_reo, name):
                continue
            name_shown = name
            # if os.path.isdir(name):
            if self.is_broken_link(name):
                name_shown += "!"
            elif self.state.is_executable(name):
                name_shown += "*"
            elif self.state.is_directory(name):
                name_shown += "/"
            mark = self.state.get_mark(name)
            result.append(Entry(mark, " ", name, name_shown))
        self.state.table = result
        self.state.stale = False
        return result

    def compile_reos(self):
        if self.ignore_reos is not None:
            return
        self.ignore_reos = []
        import re
        pattern = "^\\..*"  # dot files
        reo = re.compile(pattern)
        self.ignore_reos.append(reo)
        for pattern in self.state.fs_ignores:
            try:
                reo = re.compile(pattern)
            except Exception as e:
                self.state.display.warn("bad ignore pattern: '%s' " %
                                        pattern, timeout=5)
                self.state.display.warn("error: %s " % str(e), timeout=5)
                continue
            self.ignore_reos.append(reo)

    def ignored(self, filename):
        for reo in self.ignore_reos:
            match = reo.search(filename)
            if match is not None:
                return True
        return False

    def add(self):
        self.display.warn("Invalid operation!")

    def diff(self):
        self.display.warn("Invalid operation!")

    def commit(self):
        self.display.warn("Invalid operation!")

    def revert(self, filename):
        self.display.warn("Invalid operation!")

    def is_broken_link(self, filename):
        # https://stackoverflow.com/questions/20794/find-broken-symlinks-with-python
        if self.state.is_link and not os.path.exists(filename):
            return True
        return False