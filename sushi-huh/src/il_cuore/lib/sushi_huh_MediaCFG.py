#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_MediaCFG.py is part of Sushi, huh?.
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

# Module for manage media.cfg type files.

import os
import urllib.parse

from sushi_huh_INIFile import INIFile
from sushi_huh_Commons import Commons

class MediaCFG(dict):
    """
    __init__(mirror='', cfg_file='')

    mirror   = Mirror to CFG file.
    cfg_file = CFG file.
    """
    def __init__(self, repo='', fp_media_cfg=None):
        self.commons = Commons()

        if fp_media_cfg == None:
            return

        self.ini_file = INIFile(fp_media_cfg)

        for tag in self.ini_file:
            if 'name' in self.ini_file[tag]:
                self[repo + '/' + self.ini_file[tag]['name'][0]] = {}
                self[repo + '/' + self.ini_file[tag]['name'][0]]['name'] = tag

                if 'updates_for' in self.ini_file[tag]:
                    self[repo + '/' + self.ini_file[tag]['name'][0]]['updates_for'] = self.ini_file[self.ini_file[tag]['updates_for'][0]]['name'][0]

                if 'noauto' in self.ini_file[tag]:
                    self[repo + '/' + self.ini_file[tag]['name'][0]]['enabled'] = False
                else:
                    self[repo + '/' + self.ini_file[tag]['name'][0]]['enabled'] = True

    """
    make_path(mirror='', relative='') -> (str, str)

    Return the full path from the mirror and the relative path.

    mirror   = Mirror path.
    relative = Relative path.
    """
    def get_media_info_paths(self, mirror='', path='', relative=''):
            url = self.commons.urljoin(mirror, 'media', relative)

            if '../' in relative:
                path = '/'.join([path, relative.replace('../', '')])
            else:
                path = '/'.join([path, 'media', relative])

            return url, path
