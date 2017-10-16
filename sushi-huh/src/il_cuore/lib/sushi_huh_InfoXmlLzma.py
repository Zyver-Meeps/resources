#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_InfoXmlLzma.py is part of Sushi, huh?.
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

# LZMA info extractor.

import xml.dom.minidom
from sushi_huh_LZMA import LZMA

class InfoXmlLzma(dict):
    """
    __init__(filename='')

    filename = File to extract.
    """
    def __init__(self, filename=''):
        lzma = LZMA()

        info_xml = xml.dom.minidom.parseString(lzma.decode(filename))
        info = info_xml.getElementsByTagName('info')

        for index in range(len(info)):
            description = info[index].toxml()
            description = description.replace('</info>', '')
            description = description[description.find('>') + 1:]
            self[info[index].attributes['fn'].value + '.rpm'] = description
