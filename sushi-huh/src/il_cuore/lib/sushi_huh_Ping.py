#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_Ping.py is part of Sushi, huh?.
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

# Check the availability of a list of URLs and collect information about the size and delay of the resources.

try:
    import urllib.request as urllib_23
except:
    import urllib2 as urllib_23

import threading
import time
import sys

from sushi_huh_Commons import Commons

class Ping:
    """
    __init__(urls=[], timeout=None)

    urls = List of URLs to check.
    timeout = Connection timeout.
    """
    def __init__(self, urls=[], timeout=None):
        self.commons = Commons()
        self.timeout = timeout
        ping_threads = []
        self.ping_results = {}

        for url in set(urls):
            ping_thread = threading.Thread(target=self.do_ping, kwargs={'url': url})
            ping_threads += [ping_thread]
            ping_thread.start()

        for ping_thread in ping_threads:
            ping_thread.join()

        for url in self.ping_results:
            if self.ping_results[url] == [None, None]:
                self.do_ping(url)

    """
    do_ping(self, url='') -> None

    Check if a URL exist.

    url = URL to check.
    """
    def do_ping(self, url=''):
        if self.timeout == None:
            timeout = self.commons['url_request_timeout']
        else:
            timeout = self.timeout

        try:
            t0 = time.time()
            ourl = urllib_23.urlopen(url, None, timeout)

            try:
                size = int(ourl.info().get('Content-Length'))
            except:
                size = None

            ourl.close()
            delay = time.time() - t0
        except:
            size = None
            delay = None

        self.ping_results[url] = [size, delay]
