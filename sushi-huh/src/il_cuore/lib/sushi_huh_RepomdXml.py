#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_RepomdXml.py is part of Sushi, huh?.
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

# repomd.xml info extractor.

import xml.sax
import xml.sax.handler

class RepomdXml(xml.sax.handler.ContentHandler):
    """
    __init__(filename='')

    filename = File to parse.
    """
    def __init__(self, filename=''):
        self.catch_location = {'location': 'location'}
        self.primary_xml_gz_file = ''
        self.allfiles = []

        try:
            xml.sax.parse(open(filename), self)
        except:
            pass

    """
    startElement(name, attrs) -> None

    Callback function.
    """
    def startElement(self, name, attrs):
        try:
            location = self.catch_location[name]
            attr = attrs.getValue('href')
            self.allfiles += [attr]

            if 'primary.xml.gz' in attr:
                self.primary_xml_gz_file = attr
        except:
            pass
