#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_AvailableStatus.py is part of Sushi, huh?.
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

# Extract the provides from Debian systems.

class AvailableStatus:
    def __init__(self, filename=''):
        # Convert to valid comparison symbols
        self.replaces = {' (= ' : ' (== ', ' (<< ': ' (< ', ' (>> ': ' (> '}

        try:
            f = open(filename, 'r')
            data = f.read()
            f.close()
        except:
            return

        # The information of each package is divided by two new lines.
        packages_info = data.split('\n\n')
        packages_info = packages_info[: len(packages_info) - 1]
        self.packages = []
        self.provides = {}

        # for each  package...
        for package_info in packages_info:
            lines = package_info.split('\n')
            package = {}
            cur_tag = ''

            # for each package information field...
            for line in lines:
                if line[0] == ' ' or line[0] == '\t': # is part of a multiline field.
                    # Append the new line to the current (key, value) pair.
                    package[cur_tag] += '\n' + line
                else: # is a single line field.
                    # Split in (key, value) pair.
                    key, value = line.split(': ', 1)
                    cur_tag = key
                    package[cur_tag] = value

            # Obtains the name of the package.
            try:
                filename = package['Filename'][package['Filename'].rfind('/') + 1:]
            except:
                filename = ''.join([package['Package'], '_', package['Version'], '_', package['Architecture'], '.deb'])

            # Append it to packages and provides lists.
            self.packages += [filename]
            self.provides[filename.split('_')[0]] = package['Version']

        self.packages = sorted(set(self.packages))
