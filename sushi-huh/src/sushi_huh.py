#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh.py is part of Sushi, huh?.
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
#
# Main module.

import os
import sys

# The paths were are located the Python modules.
folders = ['lib']

# Import the paths.
for folder in folders:
    path = os.path.join('il_cuore', folder)

    if not path in sys.path:
        sys.path += [path]

from sushi_huh_Commons import Commons
from sushi_huh_MainServer import MainServer

if __name__ == "__main__":
    commons = Commons()
    servers = [MainServer(commons['server_port'], True)]

    for server in servers:
        server.start()

    for server in servers:
        server.join()
