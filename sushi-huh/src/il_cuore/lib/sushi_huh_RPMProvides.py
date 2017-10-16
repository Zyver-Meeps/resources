#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_RPMProvides.py is part of Sushi, huh?.
#
# Sushi, huh? is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sushi, huh? is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sushi, huh?.  If not, see <http://www.gnu.org/licenses/>.
#
# Email   : hipersayan_x@users.sourceforge.net
# Web-Site: http://sushi-huh.sourceforge.net/

# Read the provides of a system.

import subprocess

class RPMProvides:
    def __init__(self):
        self.packages = []
        self.provides = {}

        # Read the packages installed in a system.
        cmd_packages = ['rpm', '-qa', '--qf', '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}.rpm"\n"']
        cmd = subprocess.Popen(cmd_packages, stdout=subprocess.PIPE)
        self.packages = sorted(package.strip().decode().replace('"', '') for package in cmd.stdout.read().split(b'\n'))
        del self.packages[0]

        # Read the provides of a system.
        cmd_provides = ['rpm', '-qa', '--provides']
        cmd = subprocess.Popen(cmd_provides, stdout=subprocess.PIPE)
        self.provides = [self.split_dep(provide.strip().decode().replace('"', '')) for provide in cmd.stdout.read().split(b'\n')]

        #self.provides = {provide[0]: provide[1] for provide in self.provides}
        # Backport ->
        self._provides = {}

        for provide in self.provides:
            self._provides[provide[0]] = provide[1]

        self.provides = self._provides
        # <-

        del self.provides['']

    """
    split_dep(dep='')

    Split a string of dependencies.

    dep = string of dependencies.
    """
    def split_dep(self, dep=''):
        if ' = ' in dep:
            sdep = dep.split(' = ')
        else:
            sdep = [dep, '']

        return sdep
