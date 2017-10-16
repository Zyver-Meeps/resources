#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_Downloader.py is part of Sushi, huh?.
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

# Sushi, huh? download server.

import os
import sys

try:
    import urllib.request as urllib_23
except:
    import urllib as urllib_23

import threading
import traceback
import tempfile

from sushi_huh_Commons import Commons
from sushi_huh_INIFile import INIFile
from sushi_huh_Ping import Ping

class Downloader():
    """
    __init__(cbk_download_info_func=None, cbk_download_end_func=None)

    cbk_download_info_func = None
    cbk_download_end_func = None
    """
    def __init__(self, cbk_download_info_func=None, cbk_download_end_func=None):
        self.commons = Commons()

        # Download information.
        self.download_info = {
        'total_download_files': 0,
        'downloaded_files': 0,
        'total_download_bytes': 0,
        'downloaded_bytes': 0,
        'current_file_url': '',
        'current_file_path': '',
        'current_tmp_file': ''}

        # Get sussesfull downloads.
        self.downloaded = INIFile(os.path.join(self.commons['settings_path'], 'downloads.ini'))
        # Get failed downloads.
        self.failed = INIFile(os.path.join(self.commons['settings_path'], 'failed.ini'))

        self.exit = False
        self.clean_downloads = True
        self.downloads = {}
        self.no_delete = set()
        self.cbk_download_info_func = cbk_download_info_func
        self.cbk_download_end_func = cbk_download_end_func
        self.dwn_thr = threading.Thread(target=self.download_thread)
        self.dwn_thr.start()

    """
    download_thread() -> None

    Create a thread to download the packages.
    """
    def download_thread(self):
        while not self.exit:
            # If no more download in the download list, clear download info.
            if self.downloads == {} and self.clean_downloads:
                self.download_info = {
                'total_download_files': 0,
                'downloaded_files': 0,
                'total_download_bytes': 0,
                'downloaded_bytes': 0,
                'current_file_url': '',
                'current_file_path': '',
                'current_tmp_file': ''}

                if self.cbk_download_info_func != None:
                    self.cbk_download_info_func(self.download_info)

            downloads_copy = self.downloads.copy()

            for filename in downloads_copy:
                if self.downloads[filename] == None:
                    # If the file is allready downloaded, remove it from download list.
                    if not filename in self.no_delete:
                        del self.downloads[filename]
                else:
                    url = self.downloads[filename]
                    path = self.commons.rel2abs(filename)
                    tmp = self.commons.get_temp(path)

                    self.download_info['current_file_url'] = url
                    self.download_info['current_file_path'] = path
                    self.download_info['current_tmp_file'] = tmp

                    try:
                        self.retrieve(url, tmp)
                        self.commons.copy_move(tmp, path, True)
                        self.downloaded.set_pair('files', filename, [self.downloads[filename]])
                    except:
                        self.failed.set_pair('files', filename, [self.downloads[filename]])

                    self.downloads[filename] = None
                    self.download_info['downloaded_files'] += 1
                    self.downloaded.save()
                    self.failed.save()

            if downloads_copy != self.downloads and self.cbk_download_end_func != None:
                self.cbk_download_end_func()

    """
    retrieve(url, path) -> None

    Download a file from url to path.

    url = Source URL.
    path = Dest path.
    """
    def retrieve(self, url='', path=''):
        # Number of bytes to read each time.
        buff_size = 1024

        # Open the Source file.
        in_stream = urllib_23.urlopen(url)

        # Open the Dest file.
        out_stream = open(path, 'wb')

        # Read with a buffer size of buff_size.
        data = in_stream.read(buff_size)

        while (data != b'') and (not self.exit):
            out_stream.write(data)
            self.download_info['downloaded_bytes'] += len(data)
            data = in_stream.read(buff_size)

            if self.cbk_download_info_func != None:
                self.cbk_download_info_func(self.download_info)

        out_stream.close()
        in_stream.close()

        if self.exit:
            os.remove(path)

    """
    get_files(files={}, wait=False, openfiles=False, cache=False, filemode='rb') -> {filename: fileptr}

    files = Files to retrieve {filename: url}.
    wait = Wait until all downloads are finished.
    openfiles = Open files after download.
    cache = In cache mode the files are downloaded only once.
    filemode = File open mode, if openfiles=True.
    """
    def get_files(self, files={}, wait=False, openfiles=False, cache=False, filemode='rb'):
        # Unneeded
        # -> Backport
        _fs = {}

        for filename in files:
            if type(files[filename]) == type([]):
                _fs[str(filename)] = [str(files[filename][0]), files[filename][1]]
            else:
                _fs[str(filename)] = str(files[filename])

        files = _fs
        # <-

        # Dont clean the download list until the new files was added.
        self.clean_downloads = False

        # First check if the URLs exist.
        ping_urls = []

        for filename in files:
            if type(files[filename]) == type(''):
                ping_urls += [files[filename]]

        pinger = Ping(ping_urls)

        total_download_files = 0
        total_download_bytes = 0
        download_files = {}

        for filename in files:
            if type(files[filename]) == type(''):
                url = files[filename]
                filesize = pinger.ping_results[url][0]
            else:
                url = files[filename][0]
                filesize = files[filename][1]

            if filesize != None and (not cache or (cache and not os.path.exists(self.commons.rel2abs(filename)))):
                download_files[filename] = url
                total_download_files += 1
                total_download_bytes += filesize
            else:
                download_files[filename] = None
                self.failed.set_pair('files', filename, [url])

            if wait:
                self.no_delete.add(filename)

        self.failed.save()
        self.download_info['total_download_files'] += total_download_files
        self.download_info['total_download_bytes'] += total_download_bytes
        self.downloads.update(download_files)

        if wait:
            w = True

            while w:
                ready = True

                for filename in files:
                    if self.downloads[filename] != None:
                        ready &= False

                if ready:
                    w = False

            for filename in files:
                self.no_delete.discard(filename)

        fp_list = {}

        if openfiles:
            for filename in files:
                full_path = self.commons.rel2abs(filename)

                try:
                    fp_list[filename] = open(full_path, filemode)
                except:
                    fp_list[filename] = None

        # All files was added, now the download list can be cleaned.
        self.clean_downloads = True

        return fp_list
