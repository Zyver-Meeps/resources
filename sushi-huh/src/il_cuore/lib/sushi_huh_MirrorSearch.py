#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Sushi, huh? offline package downloader for GNU/Linux systems
## Copyright (C) 2008  Gonzalo Exequiel Pedone
##
## sushi_huh_MirrorSearch.py is part of Sushi, huh?.
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
##
## Code  writer: zboy (Zweet Boy)
## Email       : zboy@users.sourceforge.net
##

# Returns a mirror list of servers for Ubuntu.

import sys
import urllib.request
import traceback

class UbuntuMirrors():
    def get_mirror_list():
        pass
        # ...
        #foreach mirror_name:
        #    mirrors[mirror_name] = self.get_urls('https://launchpad.net/ubuntu/+archivemirrors')
        # ...

    """
    get_urls(url='') -> {}

    Returns a dictionary with the mirrors.

    url = URL to parse.
    """
    def get_urls(self, url=''):
        self._mirror_name = ""
        self.mirror_list = []
        self.mirrors_dict = {}

        # This attribute prevents to add a void mirror name.
        self._first_time_lock = True

        # Web url to parse.
        try:
            fw = urllib.request.urlopen(url)
        except:
            type_, value, traceback_ = sys.exc_info()
            traceback.print_exception(type_, value, traceback_)

        for line in fw.read().decode().split('\n'):
            if "<a href=" in line.lower() and\
               "</a>"     in line.lower() and\
               "+mirror"  in line.lower():
                posi = line.rfind("\">")

                if posi != -1:
                    posi += len("\">")
                    posf = line.lower().find("</a>", posi)

                    temp_name = line[posi:posf]
                    #print "-------------------------------------------"
                    #print "temp_name: {0}".format(temp_name)
                    #print "mirror_name: {0}".format(self._mirror_name)

                    if not self._first_time_lock:
                        if self._mirror_name != temp_name:
                            self.mirrors_dict[self._mirror_name] =\
                            self.mirror_list
                            self._mirror_name = temp_name
                            self.mirror_list = []
                    else:
                        self._first_time_lock = False
                        self._mirror_name = temp_name
            else:
                # Extract the mirrors.
                if ">http<"  in line or\
                   ">ftp<"   in line or\
                   ">rsync<" in line:
                    posi = line.lower().rfind("<a href=\"")
                    if posi != -1:
                        posi += len("<a href=\"")
                        posf = line.find("\">", posi)

                        self.mirror_list.append(line[posi:posf])

        return self.mirrors_dict # Must be a list of urls []

#um = UbuntuMirrors()
#print(um.get_mirror('https://launchpad.net/ubuntu/+archivemirrors'))

#python3.1 sushi_huh_MirrorSearch.py
#
#{
# 'SUNET': ['http://ftp.sunet.se/pub/os/Linux/distributions/ubuntu/ubuntu/', 'ftp://ftp.sunet.se/pub/os/Linux/distributions/ubuntu/ubuntu/'],
# 'BJTU': ['http://mirror.bjtu.edu.cn/ubuntu/', 'ftp://mirror.bjtu.edu.cn/ubuntu/'],
# 'Open Consultants': ['http://ubuntu.eriders.ge/ubuntu/', 'ftp://ubuntu.eriders.ge/ubuntu/'],
# 'University Of Kent UK Mirror Service': ['http://www.mirrorservice.org/sites/archive.ubuntu.com/ubuntu/', 'ftp://ftp.mirrorservice.org/sites/archive.ubuntu.com/ubuntu/', 'rsync://rsync.mirrorservice.org/archive.ubuntu.com/ubuntu/']}
#
# Must be:
#
#['http://ftp.sunet.se/pub/os/Linux/distributions/ubuntu/ubuntu/', 'ftp://ftp.sunet.se/pub/os/Linux/distributions/ubuntu/ubuntu/', 'http://mirror.bjtu.edu.cn/ubuntu/', 'ftp://mirror.bjtu.edu.cn/ubuntu/', 'http://ubuntu.eriders.ge/ubuntu/', 'ftp://ubuntu.eriders.ge/ubuntu/', 'http://www.mirrorservice.org/sites/archive.ubuntu.com/ubuntu/', 'ftp://ftp.mirrorservice.org/sites/archive.ubuntu.com/ubuntu/', 'rsync://rsync.mirrorservice.org/archive.ubuntu.com/ubuntu/']
#
