#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_SynthesisHdlistCz.py is part of Sushi, huh?.
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

# Module for manage SynthesisHdlistCz type files.

import os
import sys
import gzip

from sushi_huh_Commons import Commons

class SynthesisHdlistCz:
    """
    __init__(filename='')

    Load the synthesis.hdlist.cz type files in tables.

    filename = File to load.
    """
    def __init__(self, filename='', extras={}):
        try:
            f = gzip.open(filename)
        except:
            return

        data = ''.join([chr(c) for c in f.read()])
        f.close()

        self.commons = Commons()
        lines = []

        for l in data.split('\n'):
            if l != '':
                lines += [l]

        self.packages = []
        self.provides = {}
        self.requires = {}

        for line in lines:
            keys = line.split('@')

            if keys[1] == 'provides':
                suggests = []
                requires = []
                provs = keys[2:]
            elif keys[1] == 'obsoletes':
                obsoletes = keys[2:]
            elif keys[1] == 'conflicts':
                conflicts = keys[2:]
            elif keys[1] == 'requires':
                requires = keys[2:]
            elif keys[1] == 'suggests':
                suggests = keys[2:]
            elif keys[1] == 'summary':
                summary = keys[2]
            elif keys[1] == 'filesize':
                size = int(keys[2])
            elif keys[1] == 'info':
                filename = keys[2] + '.rpm'
                group = keys[5]
                name, version, release, arch = self.get_external_info(keys[2])

                try:
                    description = extras['ixl'][filename]
                except:
                    description = ''

                package_id = '/'.join([extras['section'], filename])
                package = [package_id, name, version, release, arch, group, 'No', extras['section'], size, summary, description, self.commons.urljoin(extras['url'], filename), '/'.join([extras['path'], filename]), 0]

                self.packages += [package]

                self.requires[package_id] = [size, [self.split_dependency(require) for require in requires], [self.split_dependency(suggest) for suggest in suggests]]

                for provide in provs:
                    prov = self.split_dependency(provide) + [package_id]

                    if prov[0] in self.provides:
                        self.provides[prov[0]] += [prov[1:]]
                    else:
                        self.provides[prov[0]] = [prov[1:]]

    """
    get_external_info(filename='')

    Split finename in (name, version, release, arch) tuple.

    filename = RPM package name.
    """
    def get_external_info(self, filename=''):
        arch = filename[filename.rfind('.') + 1:]
        filename = filename[: filename.rfind('.')]
        release = filename[filename.rfind('-') + 1:]
        filename = filename[: filename.rfind('-')]
        version = filename[filename.rfind('-') + 1:]
        name = filename[: filename.rfind('-')]

        return name, version, release, arch

    """
    split_dependency(name='') -> [str, str, str]

    Return a provide or require splited in a [name, flag, version].

    name = Name of the dependecy.
    """
    def split_dependency(self, name=''):
        flag = ''
        version = ''

        if '[' in name:
            _name = name.split('[')
            name = _name[0]

            if '*' in _name[1]:
                flag = ''
                version = ''
            else:
                version = _name[1].replace(']', '')
                version = version.split(' ')
                flag = version[0]
                version = version[1]
        else:
            flag = ''
            version = ''

        return [name, flag, version]
