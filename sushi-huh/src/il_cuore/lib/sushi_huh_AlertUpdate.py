#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_AlertUpdate.py is part of Sushi, huh?.
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

# This tool help you to update Sushi, huh? to the last version.

try:
    import urllib.request as urllib_23
except:
    import urllib as urllib_23

from sushi_huh_Commons import Commons
from sushi_huh_VersionSystem import VersionSystem

class AlertUpdate:
    def __init__(self):
        self.commons = Commons()
        version_system = VersionSystem()
        self.new_version = ''

        try:
            # Retrieve current program version information from the official web site.
            current_version = urllib_23.urlopen(self.commons.urljoin(self.commons['web_site'], 'data', 'info', 'current_version.txt'))
        except:
            return

        cur_ver = str(current_version.read())
        current_version.close()
        cur_ver = cur_ver.split('\n')[0]

        # Compare web site version with local version.
        if version_system.compare_versions(cur_ver, '>', self.commons['program_version']):
            self.new_version = cur_ver
