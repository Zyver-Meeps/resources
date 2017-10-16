#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_PrimaryXmlGz.py is part of Sushi, huh?.
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

# Module for manage PrimaryXmlGz type files.

import sys
import gzip
import xml.sax
import xml.sax.handler

from sushi_huh_Commons import Commons
from sushi_huh_Table import Table
from sushi_huh_INIFile import INIFile

class PrimaryXmlGz(xml.sax.handler.ContentHandler):
    """
    __init__(filename='', extras={})

    filename = File name to parse.
    extras = Extra values to construct the packages table.
    """
    def __init__(self, filename='', extras={}):
        self.commons = Commons()
        main_ini_file = INIFile(self.commons['ini_file'])
        main_arch = main_ini_file['DEFAULT']['Arch'][0]

        self.flags = {'LE': '<=', 'GE': '>=', 'EQ': '==', 'LT': '<', 'GT': '>'}
        self.archs_ix86 = {}

        for i in range(3, 7):
            self.archs_ix86[str(i).join(['i', '86'])] = ''

        self.archs_ix86['noarch'] = ''
        self.archs_Amd64 = {'x86_64': '', 'noarch': ''}
        self.archs_ia64 = {'ia64': '', 'noarch': ''}
        self.allowed_archs = []

        if main_arch in self.archs_ix86:
            self.allowed_archs = self.archs_ix86
        elif main_arch in self.archs_Amd64:
            self.allowed_archs = self.archs_Amd64
        elif main_arch in self.archs_ia64:
            self.allowed_archs = self.archs_ia64

        self.package = {}
        self.package_tag = {'package': ''}
        self.entry_tag = {'rpm:entry': ''}
        self.arch_tag = {'arch': ''}
        self.provides_requires = {'rpm:provides': [], 'rpm:requires': []}
        self.catch_tags_contents = {'name': '', 'arch': '', 'summary': '', 'description': '', 'rpm:group': ''}
        self.catch_tags_attrs = {'version': ['ver', 'rel'], 'size': ['package'], 'location': ['href']}
        self.catch_content = {'False': ''}
        self.lock_arch = {'False': ''}
        self.cur_tag = ''
        self.cur_prov_req_tag = ''
        self.contents = ''
        self.extras = extras
        self.packages = []
        self.requires = {}
        self.provides = {}

        try:
            xml.sax.parse(gzip.open(filename), self)
        except:
            pass

    """
    startElement(name, attrs) -> None

    Callback function.
    """
    def startElement(self, name, attrs):
        # Im use try/except instead of if/else because is more fast.
        try:
            ok = self.lock_arch['False']

            try:
                ok = self.package_tag[name]
                self.package = {}
            except:
                pass

            try:
                ok = self.catch_tags_contents[name]
                self.package[name] = ''
                self.catch_content = {'True': ''}
                self.cur_tag = name
            except:
                pass

            try:
                for attr in self.catch_tags_attrs[name]:
                    self.package['/'.join([name, attr])] = attrs.getValue(attr)
            except:
                pass

            try:
                ok = self.provides_requires[name]
                self.provides_requires[name] = []
                self.cur_prov_req_tag = name
            except:
                pass

            try:
                ok = self.entry_tag[name]

                try:
                    flag = [self.flags[attrs.getValue('flags')], attrs.getValue('ver')]
                except:
                    flag = ['', '']

                self.provides_requires[self.cur_prov_req_tag] += [[attrs.getValue('name')] + flag]
            except:
                pass
        except:
            pass

    """
    characters(content) -> None

    Callback function.
    """
    def characters(self, content):
        try:
            ok = self.catch_content['True']
            self.contents += content
        except:
            pass

    """
    endElement(name) -> None

    Callback function.
    """
    def endElement(self, name):
        try:
            ok = self.catch_content['True']
            self.package[self.cur_tag] = self.contents
            self.catch_content = {'False': ''}
            self.cur_tag = ''
            self.contents = ''
        except:
            pass

        try:
            ok = self.arch_tag[name]

            try:
                ok = self.allowed_archs[self.package[name]]
            except:
                self.lock_arch = {'True': ''}
        except:
            pass

        try:
            ok = self.provides_requires[name]
            self.cur_prov_req_tag = ''
        except:
            pass

        try:
            ok = self.package_tag[name]

            try:
                ok = self.lock_arch['False']

                package_id = ''.join(['/', self.package['location/href']])
                package_id = '/'.join([self.extras['section'], package_id[package_id.rfind('/') + 1:]])
                size = int(self.package['size/package'])
                pkg = [package_id, self.package['name'],
                self.package['version/ver'],
                self.package['version/rel'], self.package['arch'],
                self.package['rpm:group'], 'No', self.extras['section'], size,
                self.package['summary'], self.package['description'],
                self.commons.urljoin(self.extras['url'], self.package['location/href']),
                '/'.join([self.extras['path'], self.package['location/href']]), 0]

                self.packages += [pkg]
                self.requires[package_id] = [size, self.provides_requires['rpm:requires'], []]

                for provide in self.provides_requires['rpm:provides']:
                    prov = provide + [package_id]

                    if prov[0] in self.provides:
                        self.provides[prov[0]] += [prov[1:]]
                    else:
                        self.provides[prov[0]] = [prov[1:]]
            except:
                pass

            self.lock_arch = {'False': ''}
        except:
            pass
