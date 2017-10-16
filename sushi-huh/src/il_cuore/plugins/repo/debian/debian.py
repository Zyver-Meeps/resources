#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Sushi, huh? offline package downloader for GNU/Linux systems
## Copyright (C) 2008  Gonzalo Exequiel Pedone
##
## debian.py is part of Sushi, huh?.
##
## Sushi, huh? is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## Sushi, huh? is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Sushi, huh?.  If not, see <http://www.gnu.org/licenses/>.
##
## Email   : hipersayan_x@users.sourceforge.net
## Web-Site: http://sushi-huh.sourceforge.net/

# Plugin for Debian.

import os
import sys
import traceback

from sushi_huh_INIFile import INIFile
from sushi_huh_PluginBase import PluginBase
from sushi_huh_PackagesGz import PackagesGz
from sushi_huh_PackagesDB import PackagesDB

class Plugin(PluginBase):
    def set_packmanager(self):
        sources_list_file = '/etc/apt/sources.list'
        sources_list_temp = self.commons.get_temp(sources_list_file)

        plugin_ini_file = self.get_plugin_ini_file()
        main_ini_file = self.get_main_ini_file()

        sources_list = ''
        fst = True

        for repo in main_ini_file['repo']:
            sections = []

            for section in main_ini_file['repo'][repo]:
                if main_ini_file[section]['enabled'][0] == 'True':
                    sections += [section[section.rfind('/') + 1:]]

            if sections != []:
                apt_line = 'deb file://' + os.path.join(os.path.expanduser("~"), '.sushi-huh', 'src', 'downloads', repo) + ' ' + main_ini_file['DEFAULT']['Distribution'][0] + ' ' + ' '.join(sections)

                sources_list += apt_line + '\n'

        slist_file = open(sources_list_temp, 'w')
        slist_file.write(sources_list)
        slist_file.close()

        self.commons.run_sucmd('rename \'s/\\.list$/\\.list~/\' /etc/apt/*.list;mv -f ' + sources_list_temp + ' ' + sources_list_file + ';apt-get update')

    def get_sections(self):
        main_ini_file = self.get_main_ini_file()
        plugin_ini_file = self.get_plugin_ini_file()
        plugin_ini_file.replace_keys(main_ini_file.get_defaults())
        repo_data = {}

        for repo in plugin_ini_file['sections']:
            repo_data[repo] = {}

            for section in plugin_ini_file['sections'][repo]:
                repo_sec = '/'.join([repo, section])
                repo_data[repo][repo_sec] = {}
                repo_data[repo][repo_sec]['name'] = plugin_ini_file[section]['name'][0]
                repo_data[repo][repo_sec]['enabled'] = bool(plugin_ini_file[section]['enabled'][0])

        return repo_data

    def get_tables(self):
        packages_db = PackagesDB()
        main_ini_file = self.get_main_ini_file()

        for repo in main_ini_file['repo']:
            for section in main_ini_file['repo'][repo]:
                if main_ini_file[section]['enabled'][0] == 'True':
                    packages_gz = '/'.join(['settings', repo, main_ini_file[section]['name'][0], 'binary-' + main_ini_file['DEFAULT']['Arch'][0], 'Packages.gz'])
                    packages_gz = self.commons.rel2abs(packages_gz)

                    try:
                        extras = {'section': section, 'url': main_ini_file['mirror'][repo][0], 'repo': repo}
                        pkgsgz = PackagesGz(packages_gz, extras)

                        packages_db.packages.table += pkgsgz.packages
                        packages_db.requires.update(pkgsgz.requires)

                        for provide_name in pkgsgz.provides:
                            if provide_name in packages_db.provides:
                                packages_db.provides[provide_name] += pkgsgz.provides[provide_name]
                            else:
                                packages_db.provides[provide_name] = pkgsgz.provides[provide_name]
                    except:
                        type_, value, traceback_ = sys.exc_info()
                        traceback.print_exception(type_, value, traceback_)

        packages_db.packages.sort_table('package_id')
        packages_db.close()

    def dump_repo(self):
        main_ini_file = self.get_main_ini_file()
        packages_data_files = ['Packages.bz2', 'Packages.gz', 'Release']
        files = {}

        for repo in main_ini_file['repo']:
            in_repo_url = self.commons.urljoin(main_ini_file['mirror'][repo][0], 'dists', main_ini_file['DEFAULT']['Distribution'][0])
            out_repo_dir = '/'.join(['settings', repo, 'dists', main_ini_file['DEFAULT']['Distribution'][0]])

            files['/'.join([out_repo_dir, 'Contents-' + main_ini_file['DEFAULT']['Arch'][0] + '.gz'])] = self.commons.urljoin(in_repo_url, 'Contents-' + main_ini_file['DEFAULT']['Arch'][0] + '.gz')
            files['/'.join([out_repo_dir, 'Release'])] = self.commons.urljoin(in_repo_url, 'Release')
            files['/'.join([out_repo_dir, 'Release.gpg'])] = self.commons.urljoin(in_repo_url, 'Release.gpg')

            for section in main_ini_file['repo'][repo]:
                if main_ini_file[section]['enabled'][0] == 'True':
                    in_section_url = self.commons.urljoin(main_ini_file['mirror'][repo][0], main_ini_file[section]['name'][0], 'binary-' + main_ini_file['DEFAULT']['Arch'][0])

                    out_section_dir = '/'.join(['settings', repo, main_ini_file[section]['name'][0], 'binary-' + main_ini_file['DEFAULT']['Arch'][0]])

                    for f in packages_data_files:
                        files['/'.join([out_section_dir, f])] = self.commons.urljoin(in_section_url, f)

        self.get_files(files, True, False)

    def get_mirror_list(self):
        plugin_ini_file = self.get_plugin_ini_file()
        mirror_list = {}

        for mirror in plugin_ini_file['mirror']:
            mirror_list[mirror] = [plugin_ini_file['mirror'][mirror][0]]

        return mirror_list
