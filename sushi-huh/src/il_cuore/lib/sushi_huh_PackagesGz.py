#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_PackagesGz.py is part of Sushi, huh?.
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

# Extract information from Packages.gz files.

import sys
import os
import gzip

from sushi_huh_Commons import Commons

class PackagesGz:
    """
    __init__(filename='', extras={})

    filename = File name to parse.
    extras = Extra values to construct the packages table.
    """
    def __init__(self, filename='', extras={}):
        self.commons = Commons()
        self.replaces = {' (= ' : ' (== ', ' (<< ': ' (< ', ' (>> ': ' (> '}

        try:
            f = gzip.open(filename)
            data = f.read()
            f.close()
        except:
            return

        # Each package is separated by a two new lines characters.
        packages_info = data.split(b'\n\n')
        packages_info = packages_info[: len(packages_info) - 1]
        sys.__stdout__.write(str(packages_info) + '\n')

        self.packages = []
        self.provides = {}
        self.requires = {}

        # Each package is transformed in a {key: value}.
        for package_info in packages_info:
            lines = package_info.split(b'\n')
            package = {}
            cur_tag = ''

            for line in lines:
                # This line is part of a previous multiline value.
                if ord(str(line[0])) == 32 or ord(str(line[0])) == 9:
                    try:
                        package[cur_tag] += '\n' + line.decode()
                    except:
                        package[cur_tag] += '\n' + line.decode('iso8859_15')
                # This is a line of {key: value}, and can be the first line of a multiline value.
                else:
                    key, value = line.split(b': ', 1)
                    cur_tag = key.decode()

                    try:
                        package[cur_tag] = value.decode()
                    except:
                        package[cur_tag] = value.decode('iso8859_15')

            try:
                pkgname = package['Package']
            except:
                pkgname = self.get_package(package['Filename'])

            try:
                requires = self.parse_deps(package['Depends'])
            except:
                requires = []

            try:
                suggests += self.parse_deps(package['Recommends'])
            except:
                suggests = []

            try:
                suggests += self.parse_deps(package['Suggests'])
            except:
                pass

            version, release = self.split_version_release(package['Version'])
            summary, description = self.split_summary_description(package['Description'])
            package_id = ''.join([extras['section'], '/', pkgname, '_', package['Version'], '_', package['Architecture'], '.deb'])
            url = self.commons.urljoin(extras['url'], package['Filename'])
            path = '/'.join(['downloads', extras['repo'], package['Filename']])

            # Construct the package row.
            pkg = [package_id, pkgname, version, release, package['Architecture'], package['Section'], 'No', extras['section'], int(package['Size']), summary, description, url, path, 0]

            # And add this to the table.
            self.packages += [pkg]

            self.requires[package_id] = [int(package['Size']), requires, suggests]

            provs = [[pkgname, '==', package['Version']]]

            try:
                provs += self.parse_deps(package['Provides'])
            except:
                pass

            for provide in provs:
                prov = provide + [package_id]

                if prov[0] in self.provides:
                    self.provides[prov[0]] += [prov[1:]]
                else:
                    self.provides[prov[0]] = [prov[1:]]

    """
    split_version_release(version_release='') -> (str, str)

    Split in (version, release).

    version_release = The string to split.
    """
    def split_version_release(self, version_release=''):
        if '-' in version_release:
            version = version_release[: version_release.rfind('-')]
            release = version_release[version_release.rfind('-') + 1:]
        else:
            version = version_release
            release = ''

        return version, release

    """
    split_summary_description(summary_description='') -> (str, str)

    Split in (summary, description).

    summary_description = The string to split.
    """
    def split_summary_description(self, summary_description=''):
        summary = summary_description[: summary_description.find('\n')]
        description = summary_description[summary_description.find('\n') + 1:]

        return summary, description

    """
    get_package(filename='') -> str

    Returns the name of a package.

    filename = Full file name.
    """
    def get_package(self, filename=''):
        filename = filename[filename.rfind('/') + 1:]

        return filename[: filename.find('_')]

    """
    parse_deps(deps='') -> []

    Convert a string of dependencies in a list suitable for comparison.

    deps = string of dependencies.
    """
    def parse_deps(self, deps=''):
        for replace in self.replaces:
            deps = deps.replace(replace, self.replaces[replace])

        deps = deps.replace(' | ', ', ').split(', ')
        deps = [self.split_dependency(dep) for dep in deps]

        return deps

    """
    split_dependency(name='') -> ['', '', '']

    Return a provide or require splited in a [name, flag, version].

    name = keyword.
    """
    def split_dependency(self, name=''):
        flag = ''
        version = ''

        if ' (' in name:
            _name = name.split(' (')
            name = _name[0]

            if '*' in _name[1]:
                flag = ''
                version = ''
            else:
                version = _name[1].replace(')', '')
                version = version.split(' ')
                flag = version[0]
                version = version[1]
        else:
            flag = ''
            version = ''

        return [name, flag, version]
