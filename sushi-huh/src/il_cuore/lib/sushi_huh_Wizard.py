#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_Wizard.py is part of Sushi, huh?.
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

# Sushi, huh? configuration module.

from sushi_huh_Commons import Commons
from sushi_huh_INIFile import INIFile
from sushi_huh_Pluginator import Pluginator

class Wizard:
    """
    __init__(user_defs={}, clone=False, get_files_func=None)

    user_defs = User settings.
    clone = Clone repositories?
    get_files_func = This was for an old implementation, must be removed.
    """
    def __init__(self, user_defs={}, clone=False, get_files_func=None):
        commons = Commons()
        self.main_ini_file = INIFile(commons['ini_file'])
        pluginator = Pluginator()
        self.status_keys = ['options', 'plugin', 'defaults', 'mirrors', 'repositories', 'clone', 'ready']
        self.closed = False
        self.cur_status = 0
        self.cur_status_key = self.status_keys[self.cur_status]
        self.options = {}

        # Append information about the program to the main INI file.
        if not 'program' in self.main_ini_file:
            self.main_ini_file['program'] = {}
            self.main_ini_file['program']['name'] = [commons['program_name']]
            self.main_ini_file['program']['version'] = [commons['program_version']]
            self.main_ini_file.save()

        # Default options
        if not 'options' in self.main_ini_file:
            self.main_ini_file['options'] = {}
            self.main_ini_file['options']['program_skin'] = [commons['program_skin']]
            self.main_ini_file['options']['wallpaper'] = [commons['wallpaper']]
            self.main_ini_file['options']['suggests_are_requires'] = [commons['suggests_are_requires']]
            self.main_ini_file['options']['default_lang'] = [commons['default_lang']]
            self.main_ini_file.save()

        self.cur_status += 1
        self.cur_status_key = self.status_keys[self.cur_status]

        # Set the plugin.
        if not 'plugin' in self.main_ini_file:
            if 'plugin' in user_defs:
                self.main_ini_file['plugin'] = pluginator.get_plugin_info('repo', user_defs['plugin'])
                self.main_ini_file.save()
            else:
                self.options = {'plugin': pluginator.find_plugins('repo')}

                return

        self.cur_status += 1
        self.cur_status_key = self.status_keys[self.cur_status]

        # Get plugin.
        self.plugin = pluginator.get_plugin('repo', self.main_ini_file['plugin']['plugin_name'][0])
        self.plugin.get_files = get_files_func
        plugin_ini_file = self.plugin.get_plugin_ini_file()

        # Set keys.
        if not 'DEFAULT' in self.main_ini_file:
            if 'defaults' in user_defs:
                for key in user_defs['defaults']:
                    if key in plugin_ini_file['DEFAULT']:
                        self.main_ini_file.set_pair('DEFAULT', key, [user_defs['defaults'][key]])

                self.main_ini_file.save()
            else:
                self.options = {'defaults': {'DEFAULT': plugin_ini_file['DEFAULT']}}

                for key in plugin_ini_file['DEFAULT']:
                    self.options['defaults'][key] = plugin_ini_file[key]

                return

        self.cur_status += 1
        self.cur_status_key = self.status_keys[self.cur_status]

        # Set Mirrors.
        if not 'mirror' in self.main_ini_file:
            if 'mirrors' in user_defs:
                for mirror in user_defs['mirrors']:
                    if mirror != '':
                        self.main_ini_file.set_pair('mirror', mirror, [user_defs['mirrors'][mirror]])

                self.main_ini_file.save()
            else:
                self.options = {'mirrors': self.plugin.get_mirror_list()}

                return

        self.cur_status += 1
        self.cur_status_key = self.status_keys[self.cur_status]

        # Set the sections.
        if not 'repo' in self.main_ini_file:
            if 'repositories' in user_defs:
                sections = self.plugin.get_sections()

                for repo in sections:
                    self.main_ini_file.set_pair('repo', repo, sorted(sections[repo].keys()))

                    for section in sections[repo]:
                        self.main_ini_file.set_pair(section, 'name', [sections[repo][section]['name']])

                        if 'updates_for' in sections[repo][section]:
                            self.main_ini_file.set_pair(section, 'updates_for', [sections[repo][section]['updates_for']])

                        if section in user_defs['repositories']:
                            self.main_ini_file.set_pair(section, 'enabled', [True])
                        else:
                            self.main_ini_file.set_pair(section, 'enabled', [False])

                self.main_ini_file.save()
            else:
                self.options = {'repositories': self.plugin.get_sections()}

                return

        self.cur_status += 1
        self.cur_status_key = self.status_keys[self.cur_status]

        if clone:
            self.clone_repo()

    """
    clone_repo() -> None

    Clone repositories to the flashdrive.
    """
    def clone_repo(self):
        # Dump repositories and close ini_file.
        if not 'ready' in self.main_ini_file:
            self.plugin.dump_repo()
            self.main_ini_file.set_tag('ready')
            self.main_ini_file.save()

        self.cur_status += 1
        self.cur_status_key = self.status_keys[self.cur_status]
