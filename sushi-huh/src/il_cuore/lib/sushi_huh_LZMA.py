#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_LZMA.py is part of Sushi, huh?.
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

# Decode LZMA files.

import os
import sys
import subprocess

from sushi_huh_Commons import Commons

class LZMA:
    def __init__(self):
        self.commons = Commons()

    """
    decode(filename='') -> str

    Decode a LZMA file.

    filename = Name of the file to decode.
    """
    def decode(self, filename=''):
        # If working under Windows.
        if sys.platform[:3] == 'win':
            results = subprocess.call([self.commons['lzma'], 'd', filename,
            os.path.splitext(os.path.basename(filename))[0]])
        # If working under Unix/Linux.
        else:
            results = subprocess.call([self.commons['lzma'], '-d', '-k', '-f', '-q',
            filename])

        if results == 0:
            try:
                fname = os.path.splitext(filename)[0]
                f = open(fname, 'r')
                txt = f.read()
                f.close()
                os.remove(fname)

                return txt
            except:
                return ''
        else:
            return ''
