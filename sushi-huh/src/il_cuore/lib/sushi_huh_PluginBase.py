#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_PluginBase.py is part of Sushi, huh?.
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

# This is a base for all plugins.

from sushi_huh_Commons import Commons
from sushi_huh_INIFile import INIFile

class PluginBase:
    def __init__(self):
        self.commons = Commons()

    """
    get_sections() -> {}

    Return the sections of the mirrors.
    """
    def get_sections(self):
        return {}

    """
    get_tables() -> ([], [])

    Return the table of probides and requires.
    """
    def get_tables(self):
        pass

    """
    clone_repo() -> None

    Clone the structure of the repository.
    """
    def dump_repo(self):
        pass

    def get_mirror_list(self):
        return {}

    def get_html(self):
        return ''

    """
    get_ini_file() -> {}

    Get the plugin INI file.
    """
    def get_plugin_ini_file(self):
        return INIFile(self.plugin_ini_filename)

    """
    get_main_ini_file() -> {}

    Get the Sushi, huh? INI file.
    """
    def get_main_ini_file(self):
        return INIFile(self.commons['ini_file'])
