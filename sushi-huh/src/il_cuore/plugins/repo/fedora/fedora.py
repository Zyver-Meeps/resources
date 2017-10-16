#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Sushi, huh? offline package downloader for GNU/Linux systems
## Copyright (C) 2008  Gonzalo Exequiel Pedone
##
## fedora.py is part of Sushi, huh?.
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

# Plugin for Fedora.

import os
import sys
import traceback

from sushi_huh_INIFile import INIFile
from sushi_huh_RepomdXml import RepomdXml
from sushi_huh_PluginBase import PluginBase
from sushi_huh_PrimaryXmlGz import PrimaryXmlGz
from sushi_huh_PackagesDB import PackagesDB

class Plugin(PluginBase):
    def set_packmanager(self):
        main_ini_file = self.get_main_ini_file()
        repo_yum = ''
        fst = True

        for repo in main_ini_file['repo']:
            for section in main_ini_file['repo'][repo]:
                if main_ini_file[section]['enabled'][0] == 'True':
                    if fst:
                        fst = False
                    else:
                        repo_yum += '\n'

                    name = section.replace('/', '_')

                    section_src = os.path.join(os.path.expanduser("~"), '.sushi-huh', 'src', 'downloads', repo, main_ini_file[section]['name'][0])

                    repo_yum += '[' + name + ']\nname=' + name + \
                    '\nbaseurl=file://' + section_src + \
                    '\nenabled=1\ngpgcheck=0\n'

        sources_repo_file = '/etc/yum.repos.d/' + self.commons['root_name'].replace('-', '_') + '.repo'
        sources_repo_temp = self.commons.get_temp(sources_repo_file)

        sources_repo_temp = open(sources_repo_temp, 'w')
        sources_repo_temp.write(repo_yum)
        sources_repo_temp.close()

        self.commons.run_sucmd('rename \'s/\\.repo$/\\.repo~/\' /etc/yum.repos.d/*.repo;mv -f ' + sources_repo_temp + ' ' + sources_repo_file)

    def get_sections(self):
        plugin_ini_file = self.get_plugin_ini_file()
        main_ini_file = self.get_main_ini_file()
        repo_data = {}
        keys = {}

        for key in main_ini_file['DEFAULT']:
            keys[key] = main_ini_file['DEFAULT'][key][0]

        plugin_ini_file.replace_keys(keys)

        for repo in main_ini_file['mirror']:
            repo_data[repo] = {}

            for section in plugin_ini_file['sections'][repo]:
                repo_data[repo][repo + '/' + section] = {}
                repo_data[repo][repo + '/' + section]['name'] = plugin_ini_file[section]['name'][0]

                if 'enabled' in plugin_ini_file[section]:
                    if plugin_ini_file[section]['enabled'][0] == 'True':
                        repo_data[repo][repo + '/' + section]['enabled'] = True
                    else:
                        repo_data[repo][repo + '/' + section]['enabled'] = False
                else:
                    repo_data[repo][repo + '/' + section]['enabled'] = True

        return repo_data

    def get_tables(self):
        packages_db = PackagesDB()
        main_ini_file = self.get_main_ini_file()

        for repo in main_ini_file['repo']:
            for section in main_ini_file['repo'][repo]:
                if main_ini_file[section]['enabled'][0] == 'True':
                    repodata_dir = '/'.join(['settings', repo, main_ini_file[section]['name'][0]])
                    repomd_xml = RepomdXml(os.path.join(repodata_dir, 'repodata', 'repomd.xml'))
                    url = self.commons.urljoin(main_ini_file['mirror'][repo][0], main_ini_file[section]['name'][0])
                    path = '/'.join(['download', repo, main_ini_file[section]['name'][0]])

                    try:
                        extras = {'section': section, 'url': url, 'path': path}
                        primary_xml_gz = PrimaryXmlGz(os.path.join(repodata_dir, repomd_xml.primary_xml_gz_file), extras)

                        packages_db.packages.table += primary_xml_gz.packages
                        packages_db.requires.update(primary_xml_gz.requires)

                        for provide_name in primary_xml_gz.provides:
                            if provide_name in packages_db.provides:
                                packages_db.provides[provide_name] += primary_xml_gz.provides[provide_name]
                            else:
                                packages_db.provides[provide_name] = primary_xml_gz.provides[provide_name]
                    except:
                        type_, value, traceback_ = sys.exc_info()
                        traceback.print_exception(type_, value, traceback_)

        packages_db.packages.sort_table('package_id')
        packages_db.close()

    def dump_repo(self):
        main_ini_file = self.get_main_ini_file()
        repomd_xml_file = 'repomd.xml'
        files = {}

        for repo in main_ini_file['repo']:
            for section in main_ini_file['repo'][repo]:
                if main_ini_file[section]['enabled'][0] == 'True':
                    url = self.commons.urljoin(main_ini_file['mirror'][repo][0], main_ini_file[section]['name'][0])
                    path = '/'.join(['settings', repo, main_ini_file[section]['name'][0]])

                    files['/'.join([path, 'repodata', repomd_xml_file])] = self.commons.urljoin(url, 'repodata', repomd_xml_file)

        self.get_files(files, True, False)
        files = {}

        for repo in main_ini_file['repo']:
            for section in main_ini_file['repo'][repo]:
                if main_ini_file[section]['enabled'][0] == 'True':
                    url = self.commons.urljoin(main_ini_file['mirror'][repo][0], main_ini_file[section]['name'][0])
                    path = '/'.join(['settings', repo, main_ini_file[section]['name'][0]])

                    repomd_xml = RepomdXml('/'.join([path, 'repodata', repomd_xml_file]))

                    for filename in repomd_xml.allfiles:
                        files['/'.join([path, filename])] = self.commons.urljoin(url, filename)

        self.get_files(files, True, False)

    def get_mirror_list(self):
        plugin_ini_file = self.get_plugin_ini_file()
        mirror_list = {}

        for mirror in plugin_ini_file['mirror']:
            mirror_list[mirror] = [plugin_ini_file['mirror'][mirror][0]]

        return mirror_list
