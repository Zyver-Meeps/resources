#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_Sync.py is part of Sushi, huh?.
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

# Synchronize your system with Sushi, huh?.

import os
import pickle

from sushi_huh_Commons import Commons
from sushi_huh_INIFile import INIFile
from sushi_huh_RPMProvides import RPMProvides
from sushi_huh_AvailableStatus import AvailableStatus
from sushi_huh_Pluginator import Pluginator

class Sync:
    def __init__(self):
        self.commons = Commons()
        self.main_ini_file = INIFile(self.commons['ini_file'])
        self.plugin = Pluginator().get_plugin('repo', self.main_ini_file['plugin']['plugin_name'][0])
        self.local_folder = os.path.join(os.path.expanduser("~"), '.sushi-huh')
        self.local_main_ini_file = INIFile(os.path.join(self.local_folder, 'src', 'settings', 'sushi-huh.ini'))
        self.send_files_to_pc()
        self.get_provides()

        if list(self.local_main_ini_file.keys()) == []:
            self.set_packmanager()

    """
    send_files_to_pc() -> None

    Send the files in your flash drive to your PC.
    """
    def send_files_to_pc(self):
        self.commons.copy_move(self.commons['settings_path'], os.path.join(self.local_folder, 'src', 'settings'), False)
        self.commons.copy_move(self.commons['download_path'], os.path.join(self.local_folder, 'src', 'downloads'), True)

    """
    get_provides() -> None

    Read all provides in your system.
    """
    def get_provides(self):
        packages = []
        provides = {}

        if self.main_ini_file['plugin']['repository_type'][0].lower() == 'rpm':
            rpmp = RPMProvides()
            packages = rpmp.packages
            provides = rpmp.provides
        else:
            avst = AvailableStatus('/var/lib/dpkg/available')
            packages = avst.packages
            provides = avst.provides

        pickle.dump((packages, provides), open(os.path.join(self.commons['settings_path'], 'provides.db'), 'wb'))

    """
    set_packmanager() -> None

    Configure automatically your package manager.
    """
    def set_packmanager(self):
        self.plugin.set_packmanager()
