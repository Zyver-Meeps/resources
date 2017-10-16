#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_MainServer.py is part of Sushi, huh?.
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

# Sushi, huh? local web server.

import os
import sys
import time
import socket

try:
    import urllib.request
    import urllib.parse
except:
    import urllib

import mimetypes
import webbrowser
import traceback

from sushi_huh_Commons import Commons
from sushi_huh_PhraseBook import PhraseBook
from sushi_huh_BaseServer import BaseServer
from sushi_huh_PackagesDB import PackagesDB
from sushi_huh_INIFile import INIFile
from sushi_huh_Pluginator import Pluginator
from sushi_huh_Downloader import Downloader
from sushi_huh_Sync import Sync

class MainServer(BaseServer):
    """
    post_bind_func() -> None

    This function is called after the webserver is binded.
    """
    def post_bind_func(self):
        # Open the predetermined web browser.
        print('Calling webbrowser...')
        webbrowser.open('http://localhost:' + str(self.port) + \
        '/', 2)
        print('Webbrowser ready.')
        print('')
        print('If the webbrowser wasn\'t appear but you' + \
        ' are sure is available,')
        print('open the webrowser and then copy & paste' + \
        ' this url:')
        print('')
        print('http://localhost:' + \
        str(self.port) + '/')
        print('')

        self.download_info = {
        'total_download_files': 0,
        'downloaded_files': 0,
        'total_download_bytes': 0,
        'downloaded_bytes': 0,
        'current_file_url': '',
        'current_file_path': '',
        'current_tmp_file': ''}

        # Some global enviroment variables.
        self.packages = None
        self.downloader = Downloader(self.cbk_download_info, self.cbk_download_end)

    """
    cbk_download_info(download_info={}) -> None

    Callback function.
    """
    def cbk_download_info(self, download_info={}):
        self.download_info = download_info

    """
    cbk_download_end() -> None

    Callback function.
    """
    def cbk_download_end(self):
        try:
            self.packages.update_downloades()
        except:
            type_, value, traceback_ = sys.exc_info()
            traceback.print_exception(type_, value, traceback_)

    """
    html_response_func(filename='', form={}, default_lang='en') -> (str, {})

    Pre-process the web pages.

    filename = Web page file name.
    form = Web formulary.
    default_lang = Default webpages language.
    """
    def html_response_func(self, filename='', form={}, default_lang='en'):
        web_page = ''
        extras = None

        # Apends new files to download or return the download info.
        if filename == 'il_cuore/html/downloads.html':
            packages = []

            for key in form:
                if key.startswith('pkg'):
                    packages += [form[key]]

            if packages != []:
                self.downloader.get_files(self.packages.resolve_files(packages))

            extras = {'download_info': self.download_info}
        # Close the server.
        elif filename == 'il_cuore/html/close.html':
            try:
                if self.packages != None:
                    self.packages.close()
            except:
                type_, value, traceback_ = sys.exc_info()
                traceback.print_exception(type_, value, traceback_)

            self.downloader.exit = True
        elif filename == 'il_cuore/html/packages.html':
            main_ini_file = INIFile(self.commons['ini_file'])

            if not 'packagesdb_ready' in main_ini_file:
                pluginator = Pluginator()
                plugin = pluginator.get_plugin('repo', main_ini_file['plugin']['plugin_name'][0])
                plugin.get_tables()
                main_ini_file.set_tag('packagesdb_ready')
                main_ini_file.save()

            # Open de packages database.
            if self.packages == None:
                self.packages = PackagesDB()

            if 'group' in form:
                extras = {'packages': self.packages.get_packages(form['group'])}
            else:
                groups = self.packages.get_groups()
                extras = {'groups': groups, 'packages': self.packages.get_packages(groups[0])}
        elif filename == 'il_cuore/html/search.html':
            extras = {'packages': self.packages.search([form['keyword']])}
        elif filename == 'il_cuore/html/description.html':
            extras = {'description': self.packages.get_description(form['package_id'])}
        elif filename == 'il_cuore/html/get_dependencies.html':
            packages = []

            for key in form:
                if key.startswith('pkg'):
                    packages += [form[key]]

            extras = {'dependencies': self.packages.get_dependencies(packages)}
        elif filename == 'il_cuore/html/loading_tables.html':
            extras = {'get_files': self.downloader.get_files}
        elif filename == 'il_cuore/html/wizard.html':
            extras = {'get_files': self.downloader.get_files}
        elif filename == 'il_cuore/html/sync.html':
            sync = Sync()
            self.packages.make_sync()

        return web_page, extras
