#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_UbuntuCodeName.py is part of Sushi, huh?.
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

# Try to guess the codename of the Ubuntu release from the number of version.
# Only for Ubuntu > 8.04. The number of versions must be x.y where "x" > 8 and
# "y" = 4 | 10, and supposing that the Ubuntu developpers continue to using the
# same algorithm O_Ou.

import os
import urllib.request
import html.parser

from sushi_huh_Commons import Commons

class UbuntuCodename(html.parser.HTMLParser):
    """
    __init__(urlbase='')

    urlbase = A Ubuntu mirror.
    """
    def __init__(self, urlbase=''):
        html.parser.HTMLParser.__init__(self)
        self.codenames = []
        self.commons = Commons()

        try:
            codenames_file = open(os.path.join(self.commons['settings_path'], 'ubuntu_codenames.txt'), 'r')
            self.codenames = codenames_file.read().split('\n')
            self.codenames = self.codenames[: len(self.codenames) - 1]
            codenames_file.close()
        except:
            try:
                url = urllib.request.urlopen(urlbase)
                out = url.read().decode()
                url.close()
            except:
                return

            if urlbase.startswith('ftp://'):
                for line in out.split('\r\n'):
                    self.codenames += [line[line.rfind(' ') + 1:]]
            else:
                self.feed(out)

            codenames_file = open(os.path.join(self.commons['settings_path'], 'ubuntu_codenames.txt') ,'w')

            for codename in self.codenames:
                codenames_file.write(codename + '\n')

            codenames_file.close()

    """
    handle_starttag(tag, attrs)

    Callback function.
    """
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.codenames += [attrs[0][1][: len(attrs[0][1]) - 1]]

    """
    get_codename(version=0, number=0) -> str

    Return the codename for a given version.

    version = Version number.
    number = Month number.
    """
    def get_codename(self, version=0, number=0):
        codechar = chr(89 + 2 * int(version) - int((10 - int(number)) / 6))

        for codename in self.codenames:
            try:
                if (not '-' in codename) and (codename[0] == codechar):
                    return codename
            except:
                pass

        return ''
