#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_BaseServer.py is part of Sushi, huh?.
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

# Sushi, huh? base web server.

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
import traceback
import threading

from sushi_huh_Commons import Commons
from sushi_huh_PhraseBook import PhraseBook
from sushi_huh_PyHP import PyHP

class BaseServer(threading.Thread):
    """
    __init__(port=0, make_threading=True) -> None

    Initialize the server.

    port = Server port.
    make_threading = Process the petition in a thread(True) or directly(False).
    """
    def __init__(self, port=0, make_threading=True):
        threading.Thread.__init__(self)

        # Load common functions.
        self.commons = Commons()
        self.deafult_lang = 'en'
        self.phrase_book = None

        self.port = port
        self.make_threading = make_threading

        # Close Sushi, huh?
        self.exit = False

    """
    run() -> None

    Run server thread.
    """
    def run(self):
        # Create the server socket.
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        binded = False

        # Some times python doesn't release correctly the socket,
        # then wait until socket is released.
        while not binded:
            try:
                self.server.bind(('', self.port))
                binded = True
            except:
                pass

        self.post_bind_func()
        self.server.listen(5)

        while not self.exit:
            # receive a client.
            client, client_address = self.server.accept()

            if self.make_threading:
                # Process the petition in a thread.
                thr = threading.Thread(target=self.process_client_petition, args=(client, ))
                thr.start()
            else:
                # Process the petition directly.
                self.process_client_petition(client)

        self.server.close()

    """
    process_client_petition(client=None) -> None

    Process client petitions.

    client = Client socket object.
    """
    def process_client_petition(self, client=None):
        # Read the header sended by client.
        header = self.read_header(client)
        # Obtains the file and the formulary requested by client.
        filename, form, default_lang = self.parse_header(header)

        # Load the translations.
        if self.phrase_book == None:
            self.deafult_lang = default_lang
            self.phrase_book = PhraseBook(default_lang)

        self.send_response(client, filename, form, default_lang)

    """
    send_response(client=None, filename='', form={}) -> None

    Process client petitions.

    client = Client socket object.
    filename = File name needed by client.
    form = Formulary of the client.
    """
    def send_response(self, client=None, filename='', form={}, default_lang='en'):
        # Try to guess the type of file it is.
        if filename == '/':
            mimetype = 'text/html'
        else:
            mimetype = mimetypes.guess_type(filename)[0]

        try:
            if mimetype == 'text/html':
                # This is a HTML file.
                try:
                    _file = bytes(self.html_response(filename, form, default_lang), 'utf_8')
                except:
                    _file = self.html_response(filename, form, default_lang)
            else:
                # This is a non-HTML file.
                filename = filename[1:]
                f = open(os.path.join(self.commons['sources_path'], filename.replace('/', os.sep)), 'rb')
                _file = f.read()
                f.close()

            ok = True
        except:
            # File doesn't exist.
            type_, value, traceback_ = sys.exc_info()
            traceback.print_exception(type_, value, traceback_)
            sys.__stdout__.write('File ' + filename + ' doesn\'t exist\n')
            _file = ''
            ok = False

        try:
            if ok:
                client.send(bytes('HTTP/1.0 200 OK\r\n', 'utf_8'))
            else:
                client.send(bytes('HTTP/1.0 404 FILE NOT FOUND\r\n', 'utf_8'))
        except:
            if ok:
                client.send('HTTP/1.0 200 OK\r\n')
            else:
                client.send('HTTP/1.0 404 FILE NOT FOUND\r\n')

        # Some times a file send fails due to a timeout error in the webbrowser.
        try:
            try:
                client.send(bytes('Content-Type: ' + mimetype + '\r\n', 'utf_8'))
                client.send(bytes('Content-Length: ' + str(len(_file)) + '\r\n', 'utf_8'))
                client.send(bytes('Last-Modified: ' + time.strftime('%a %b %d %H:%M:%S %Y') + '\r\n', 'utf_8'))
                client.send(bytes('\r\n', 'utf_8'))
            except:
                client.send('Content-Type: ' + mimetype + '\r\n')
                client.send('Content-Length: ' + str(len(_file)) + '\r\n')
                client.send('Last-Modified: ' + time.strftime('%a %b %d %H:%M:%S %Y') + '\r\n')
                client.send('\r\n')

            if type(_file) == type(''):
                try:
                    _file = bytes(_file, 'utf_8')
                except:
                    pass

            client.send(_file)
        except:
            type_, value, traceback_ = sys.exc_info()
            traceback.print_exception(type_, value, traceback_)
            sys.__stdout__.write('Can\'t send file ' + filename + ' to client\n')
            sys.__stdout__.write('client bussy\n')
            _file = ''

        client.close()

    """
    read_line(client=None) -> str

    Read a line from the head.

    client = Client socket object.
    """
    def read_line(self, client=None):
        # Convert bytes to string
        line = client.recv(1).decode()

        if line == '':
            return line

        while not line.endswith('\r\n'):
            line += client.recv(1).decode()

        return line

    """
    read_header(client=None) -> str

    Read full head sended by client.

    client = Client socket object.
    """
    def read_header(self, client=None):
        header = self.read_line(client)

        if header == '':
            return str(header)

        while (not header.endswith('\r\n\r\n')) and (header != '\r\n'):
            header += self.read_line(client)

        for line in header.split('\r\n'):
            if 'Content-Length:' in line:
                n_chars = line.split('Content-Length:')
                header += client.recv(int(n_chars[1]))

                return str(header)

        return str(header)

    """
    parse_header(header='') -> (filename='', form={})

    Obtains information about the file and formulary requested by client.

    header = Header string.
    filename = Name of the file requested by client.
    form = formulary data
    """
    def parse_header(self, header=''):
        default_lang = 'en'

        # Obtains the client language.
        if '\nAccept-Language: ' in header:
            lang_header = '\nAccept-Language: '
            sln = header.find(lang_header) + len(lang_header)
            eln = sln + 2
            default_lang = header[sln: eln].lower()

        form_header = header.split('\n')

        # Obtains the client forms variables.
        if form_header[len(form_header) - 1] != '':
            form_header = form_header[len(form_header) - 1]
        else:
            form_header = ''

        file_name = header.split(' ')

        # Something was wrong :S, please try to continue with your simple bourgeois life.
        if len(file_name) < 2:
            return '', {}, 'en'

        # Obtains the client forms variables by url.
        file_name = file_name[1].split('?')

        # Join client and url forms, in any case are the same.
        if len(file_name) == 2:
            if not form_header == '':
                form_header += '&'

            form_header += file_name[1]

        file_name = file_name[0]
        form = {}

        # Split the forms in (key, value) pairs.
        if form_header != '':
            for name_value in form_header.split('&'):
                name, value = name_value.split('=')

                try:
                    form[urllib.parse.unquote_plus(name)] = urllib.parse.unquote_plus(value)
                except:
                    form[urllib.unquote_plus(name)] = urllib.unquote_plus(value)

        return file_name, form, default_lang

    """
    html_response(filename='', form={}) -> str

    Load and pre-process webpages.

    filename = File name needed by client.
    form = Formulary of the client.
    """
    def html_response(self, filename='', form={}, default_lang='en'):
        if filename == '/' or filename == '/index.html':
            fname = 'il_cuore/html/index.html'
        else:
            fname = filename[1:]

        path = os.path.join(self.commons['sources_path'], fname.replace('/', os.sep))
        web_page, extra_vars = self.html_response_func(fname, form, default_lang)

        if web_page == '':
            # Process PyHP code.
            pyhp = PyHP(path, '', tr=self.phrase_book.tr, form=form, extras=extra_vars)
            web_page = pyhp.html

        if fname == 'il_cuore/html/close.html':
            self.exit = True

        return web_page

    """
    Overwriteable functions.
    """
    def post_bind_func(self):
        pass

    def html_response_func(self, filename='', form={}, default_lang='en'):
        web_page = ''
        extras = None

        return web_page, extras
