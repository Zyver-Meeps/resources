#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_Commons.py is part of Sushi, huh?.
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

# Provides general information to others modules.

import os
import sys
import tempfile

try:
    import urllib.parse as urllib_23
except:
    import urlparse as urllib_23

import subprocess

class Commons(dict):
    """
    __init__()

    Initialize the commons variables.
    """
    def __init__(self):
        # Program info.
        self['program_name'] = 'Sushi, huh?'
        self['program_version'] = '0.6.0'
        self['jquery_version'] = '1.3.2'
        self['jquery_ui_version'] = '1.7.2'
        self['root_name'] = 'sushi-huh'
        self['mantainer_mail'] = 'hipersayan.x@gmail.com'
        self['web_site'] = 'http://sushi-huh.sourceforge.net'
        self['author_name'] = 'Gonzalo Exequiel Pedone'

        # Server options.
        self['server_port'] = 7874

        # Paths.
        self['root_path'] = os.getcwd()
        self['root_path'] = self['root_path'][: self['root_path'].rfind(self['root_name'])] + self['root_name']
        self['sources_path'] = os.path.join(self['root_path'], 'src')
        self['js_path'] = os.path.join(self['sources_path'], 'il_cuore', 'js')
        self['plugins_path'] = os.path.join(self['sources_path'], 'il_cuore', 'plugins')
        self['images_path'] = os.path.join(self['sources_path'], 'il_cuore', 'images')
        self['css_path'] = os.path.join(self['sources_path'], 'il_cuore', 'css')
        self['html_path'] = os.path.join(self['sources_path'], 'il_cuore', 'html')
        self['settings_path'] = os.path.join(self['sources_path'], 'settings')
        self['download_path'] = os.path.join(self['sources_path'], 'downloads')
        self['ini_file'] = os.path.join(self['settings_path'], self['root_name'] + '.ini')
        self['lang_file'] = os.path.join(self['sources_path'], 'il_cuore', 'lang', 'lang.xml')

        self['package_status'] = ['', 'Downloaded', 'Installed']

        # Program options.
        self['suggests_are_requires'] = False
        self['program_skin'] = 'black-nori'
        self['wallpaper'] = 'wallpaper.png'
        self['default_lang'] = 'en'
        self['packages_db'] = os.path.join(self['settings_path'], 'packages.zip')
        self['url_request_timeout'] = 5

        # Binary paths.
        self['lzma_windows'] = os.path.join(self['sources_path'], 'il_cuore', 'bin', 'lzma', 'lzma.exe')
        self['lzma_unix'] = os.path.join(os.sep, 'usr', 'bin', 'lzma')

        # Set the LZMA uncompression tool.
        if sys.platform[: 3] == 'win':
            # If working under Windows.
            self['lzma'] = self['lzma_windows']
        else:
            # If working under Unix/Linux.
            self['lzma'] = self['lzma_unix']

    """
    convert_bytes(bytes=0) -> int

    Convert numeric byte size to human readable string size.

    bytes = Numeric byte size.
    """
    def convert_bytes(self, bytes=0):
        unit   = 0
        units  = ['B', 'KB', 'MB', 'GB', 'TB']
        bytes_ = bytes / 1000.0

        while bytes_ >= 1.0:
            unit  += 1
            bytes  = bytes_
            bytes_ = bytes / 1000.0

        return format(bytes, '.3g') + units[unit]

    """
    copy_move(src='', dst='', move=False, hook_func=None) -> None

    Copy/Move files or folders.

    src = Source file or folder.
    dst = Destiny file or folder.
    move = False(only copy file or folder) or True(copy file or folder and delete from souce).
    hook_func = This function receives the information about the current transfer status.
    """
    def copy_move(self, src='', dst='', move=False, hook_func=None):
        n_files = 0
        total_files = 0

        if os.path.isfile(src):
            self.copy_move_file(src, dst, move)
        else:
            for root, dirs, files in os.walk(src):
                total_files += len(files)

            for root, dirs, files in os.walk(src, False):
                for filename in files:
                    src_name = os.path.join(root, filename)
                    dst_name = src_name.replace(src, dst)

                    try:
                        hook_func(src_name, dst_name, n_files, total_files)
                    except:
                        pass

                    self.copy_move_file(src_name, dst_name, move)
                    n_files += 1

                try:
                    if move:
                        os.removedirs(root)
                except:
                    pass

            try:
                os.removedirs(src)
            except:
                pass

    """
    copy_move_file(src='', dst='', move=False) -> None

    Copy/Move one file.

    src = Source file.
    dst = Destiny file.
    move = False(only copy file) or True(copy file and delete from souce).
    """
    def copy_move_file(self, src='', dst='', move=False):
        fsrc = open(src, 'rb')

        try:
            # If the path doesn't exist create it.
            os.makedirs(os.path.dirname(dst))
        except:
            pass

        fdst = open(dst, 'wb')
        fdst.write(fsrc.read())
        fdst.close()
        fsrc.close()

        if move:
            os.remove(src)

    """
    rel2abs(path='') -> str

    Convert relative to absolute path.

    path = relative path.
    """
    def rel2abs(self, path=''):
        return os.path.join(self['sources_path'], path.replace('/', os.sep))

    """
    get_temp(filename='') -> str

    Convert filename in temporary filename.

    filename = Full path.
    """
    def get_temp(self, filename=''):
        return os.path.join(tempfile.gettempdir(), os.path.basename(filename))

    """
    urljoin(*urlparts) -> str

    Join url fragments paths.

    urlparts = Fragments paths.
    """
    def urljoin(self, *urlparts):
        url = ''

        for urlpart in urlparts:
            if (url != '') and (not url.endswith('/')):
                url += '/'

            url = urllib_23.urljoin(url, urlpart)

        return url

    """
    get_desktop_name() -> str

    Returns the desktop name. For a better look&feel purposes.
    """
    def get_desktop_name(self):
        cmd_kde = ['pidof', 'ksmserver']
        cmd_gnome = ['pidof', 'gnome-session']
        cmd_xfce = ['pidof', 'xfce-mcs-manage']

        if subprocess.Popen(cmd_kde, stdout=subprocess.PIPE).stdout.read() != b'':
            return 'kde'
        elif subprocess.Popen(cmd_gnome, stdout=subprocess.PIPE).stdout.read() != b'':
            return 'gnome'
        elif subprocess.Popen(cmd_xfce, stdout=subprocess.PIPE).stdout.read() != b'':
            return 'xfce'
        else:
            return '?'

    """
    run_sucmd(cmd='') -> str

    Run command as administrator.

    cmd = Command to run.
    """
    def run_sucmd(self, cmd=''):
        kdesudo = ['kdesudo', '-c']
        kdesu = ['kdesu', '-c']
        gksu = ['gksu']
        gksudo = ['gksudo']

        if self.get_desktop_name() == 'kde':
            if os.path.exists('/usr/bin/kdesudo'):
                su = kdesudo
            elif os.path.exists('/usr/bin/kdesu'):
                su = kdesu
            elif os.path.exists('/usr/bin/gksu'):
                su = gksu
            else:
                su = gksudo
        else:
            if os.path.exists('/usr/bin/gksu'):
                su = gksu
            elif os.path.exists('/usr/bin/gksudo'):
                su = gksudo
            elif os.path.exists('/usr/bin/kdesudo'):
                su = kdesudo
            else:
                su = kdesu

        if su[0][0] == 'k':
            return subprocess.Popen(su + [cmd], stdout=subprocess.PIPE).stdout.read()
        else:
            output = ''

            for c in cmd.split(';'):
                output += subprocess.Popen(su + [c], stdout=subprocess.PIPE).stdout.read()

            return output
