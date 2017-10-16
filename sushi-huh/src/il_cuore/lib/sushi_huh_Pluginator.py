#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_Pluginator.py is part of Sushi, huh?.
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

# Plugin loader.

import os
import sys

from sushi_huh_Commons import Commons
from sushi_huh_INIFile import INIFile

class Pluginator:
    def __init__(self):
        self.commons = Commons()

    """
    find_plugins() -> {}

    Return all available plugins.
    """
    def find_plugins(self, where=''):
        plugins = {}

        # Scansfor all folders in self.commons['plugins_path'].
        for plugin in os.listdir(os.path.join(self.commons['plugins_path'], where)):
            info_ini = INIFile(os.path.join(self.commons['plugins_path'], where, plugin, 'info.ini'))

            if info_ini['plugin']['enabled'][0] == 'True':
                # Obtains the plugin info.
                plugins[plugin] = info_ini['plugin']

        return plugins

    """
    get_plugin(plugin_name='') -> plugin

    Get the needed plugin.

    plugin_name = Plugin name.
    """
    def get_plugin(self, where='', plugin_name='', import_path=True):
        plugin_path = os.path.join(self.commons['plugins_path'], where, plugin_name)

        # Import the plugin.
        info_file = str(os.path.join(plugin_path, 'info.ini'))
        info = INIFile(info_file)

        if not plugin_path in sys.path:
            sys.path += [plugin_path]

        plugin = __import__(info['plugin']['main_file'][0][: info['plugin']['main_file'][0].rfind('.')]).Plugin()
        plugin.plugin_ini_filename = info_file

        if not import_path:
            sys.path.remove(plugin_path)

        return plugin

    """
    get_plugin_info(plugin_name='') -> {}

    Get the plugin info.

    plugin_name = Plugin name.
    """
    def get_plugin_info(self, where='', plugin_name=''):
        return INIFile(os.path.join(self.commons['plugins_path'], where, plugin_name, 'info.ini'))['plugin']
