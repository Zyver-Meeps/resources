#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# mandriva.py is part of Sushi, huh?.
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

# Plugin for Mandriva.

import os
import sys
import traceback
import subprocess

from sushi_huh_INIFile import INIFile
from sushi_huh_MediaCFG import MediaCFG
from sushi_huh_PluginBase import PluginBase
from sushi_huh_SynthesisHdlistCz import SynthesisHdlistCz
from sushi_huh_InfoXmlLzma import InfoXmlLzma
from sushi_huh_PackagesDB import PackagesDB
from sushi_huh_Ping import Ping

class Plugin(PluginBase):
    def set_packmanager(self):
        main_ini_file = self.get_main_ini_file()
        media_cfg_file = MediaCFG()
        cmds = ''
        fst = True

        for repo in main_ini_file['repo']:
            for section in main_ini_file['repo'][repo]:
                if main_ini_file[section]['enabled'][0] == 'True':
                    repo_src = os.path.join(os.path.expanduser("~"), '.sushi-huh', 'src', 'downloads')
                    url, path = media_cfg_file.get_media_info_paths(repo,
                    main_ini_file['mirror'][repo][0], repo_src,
                    main_ini_file[section]['name'][0])
                    repo_name = repo.replace('/', '_')

                    if fst:
                        fst = False
                    else:
                        cmds += ';'

                    cmds += 'urpmi.addmedia ' + repo_name + ' file://' + path + ';urpmi.update ' + repo_name

        self.commons.run_sucmd(cmds)

    def get_sections(self):
        main_ini_file = self.get_main_ini_file()
        plugin_ini_file = self.get_plugin_ini_file()
        files = {}

        for repo in plugin_ini_file['section']:
            files['/'.join(['settings', repo, plugin_ini_file['section'][repo][0]])] = '/'.join([main_ini_file['mirror'][repo][0], plugin_ini_file['section'][repo][0]])

        fp_media_cfg = self.get_files(files, True, True)
        repo_data = {}

        for repo in plugin_ini_file['section']:
            repo_data[repo] = MediaCFG(repo, fp_media_cfg['/'.join(['settings', repo, plugin_ini_file['section'][repo][0]])])

        return repo_data

    def get_tables(self):
        packages_db = PackagesDB()
        main_ini_file  = self.get_main_ini_file()
        media_cfg_file = MediaCFG()

        for repo in main_ini_file['repo']:
            for section in main_ini_file['repo'][repo]:
                if main_ini_file[section]['enabled'][0] == 'True':
                    url, path = media_cfg_file.get_media_info_paths(main_ini_file['mirror'][repo][0], '/'.join(['settings', repo]), main_ini_file[section]['name'][0])
                    abs_path = self.commons.rel2abs(path)

                    shdlcz_path = os.path.join(abs_path, 'media_info', 'synthesis.hdlist.cz')
                    ixl_path = os.path.join(abs_path, 'media_info', 'info.xml.lzma')

                    try:
                        ixl = InfoXmlLzma(ixl_path)
                        extras = {'ixl': ixl, 'section': section, 'url': url, 'path': path.replace('settings/', 'downloads/')}
                        shdlcz = SynthesisHdlistCz(shdlcz_path, extras)
                        packages_db.packages.table += shdlcz.packages
                        packages_db.requires.update(shdlcz.requires)

                        for provide_name in shdlcz.provides:
                            if provide_name in packages_db.provides:
                                packages_db.provides[provide_name] += shdlcz.provides[provide_name]
                            else:
                                packages_db.provides[provide_name] = shdlcz.provides[provide_name]
                    except:
                        type_, value, traceback_ = sys.exc_info()
                        traceback.print_exception(type_, value, traceback_)

        packages_db.packages.sort_table('package_id')
        packages_db.close()

    def dump_repo(self):
        main_ini_file = self.get_main_ini_file()
        plugin_ini_file = self.get_plugin_ini_file()
        media_cfg_file = MediaCFG()
        filenames = ['synthesis.hdlist.cz', 'info.xml.lzma']
        files = {}

        for repo in main_ini_file['repo']:
            for section in main_ini_file['repo'][repo]:
                if main_ini_file[section]['enabled'][0] == 'True':
                    url, path = media_cfg_file.get_media_info_paths(main_ini_file['mirror'][repo][0], '/'.join(['settings', repo]), main_ini_file[section]['name'][0])

                    for f in filenames:
                        files['/'.join([path, 'media_info', f])] = '/'.join([url, 'media_info', f])

        self.get_files(files, True, False)

    def get_mirror_list(self):
        plugin_ini_file = self.get_plugin_ini_file()
        main_ini_file = self.get_main_ini_file()
        plugin_ini_file.replace_keys(main_ini_file.get_defaults())

        mirror_list_urls = {}

        for mirror in plugin_ini_file['mirror_list']:
            filename = plugin_ini_file['mirror_list'][mirror][0]
            filename = filename[filename.rfind('/') + 1:]
            mirror_list_urls['/'.join(['settings', mirror, filename])] = plugin_ini_file['mirror_list'][mirror][0]

        fp_mirror_list = self.get_files(mirror_list_urls, True, True, False, 'r')
        mirror_list = {}

        for mirror in plugin_ini_file['mirror_list']:
            filename = plugin_ini_file['mirror_list'][mirror][0]
            filename = filename[filename.rfind('/') + 1:]
            fp = fp_mirror_list['/'.join(['settings', mirror, filename])]

            try:
                data = fp.read()
            except:
                continue

            fp.close()

            for mirror_opt in data.split('\n'):
                if mirror_opt == '':
                    break

                _mirror_opt = {}
                mirror_opt = mirror_opt.split(',')

                for key in mirror_opt:
                    _key = key.split('=')
                    _mirror_opt[_key[0]] = _key[1]

                mirror_opt = _mirror_opt

                protocol = mirror_opt['url'].split(':')
                protocol = protocol[0]

                if (mirror_opt['type'] == 'distrib') and ((protocol == 'ftp') or \
                (protocol == 'http')):
                    if mirror in mirror_list:
                        mirror_list[mirror] += [mirror_opt['url']]
                    else:
                        mirror_list[mirror] = [mirror_opt['url']]

        for mirror in mirror_list:
            pinger = Ping(mirror_list[mirror])
            valid_urls = []

            for url in pinger.ping_results:
                if pinger.ping_results[url][1] != None:
                    valid_urls += [url]

            mirror_list[mirror] = sorted(valid_urls)

        return mirror_list
