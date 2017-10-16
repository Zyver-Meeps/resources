#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_PhraseBook.py is part of Sushi, huh?.
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
# Email   : hipersayan.x@gmail.com
# Web-Site: http://sushi-huh.sourceforge.net/

# Translation system.

import xml.sax
import xml.sax.handler

from sushi_huh_Commons import Commons

class PhraseBook(xml.sax.handler.ContentHandler, dict):
    """
    __init__(os_lang='en')

    os_lang = Default language.
    """
    def __init__(self, os_lang='en'):
        self.commons = Commons()
        self.valid_chars = {}

        for i in range(0, 127):
            self.valid_chars[chr(i)] = chr(i)

        self.os_lang = os_lang
        self.default_lang = ''
        self.catch_content = False
        self.contents = ''
        self.cur_src_phrase = ''
        self.cur_dst_phrase = ''

        try:
            xml.sax.parse(open(self.commons['lang_file']), self)
        except:
            pass

    """
    startElement(name, attrs) -> None

    Callback function.
    """
    def startElement(self, name, attrs):
        if name == 'default_lang':
            self.catch_content = True

        if name == self.default_lang:
            self.catch_content = True

        if name == self.os_lang:
            self.catch_content = True

        if name == 'phrase':
            self.cur_src_phrase = ''
            self.cur_dst_phrase = ''

    """
    characters(content) -> None

    Callback function.
    """
    def characters(self, content):
        if self.catch_content:
            self.contents += content

    """
    endElement(name) -> None

    Callback function.
    """
    def endElement(self, name):
        if name == 'default_lang':
            self.default_lang = self.contents
            self.catch_content = False
            self.contents = ''

        if name == self.default_lang:
            self.cur_src_phrase = self.contents
            self.catch_content = False
            self.contents = ''

        if name == self.os_lang:
            self.cur_dst_phrase = self.contents
            self.catch_content = False
            self.contents = ''

        if name == 'phrase':
            if self.cur_dst_phrase == '':
                self[self.cur_src_phrase] = self.cur_src_phrase
            else:
                self[self.cur_src_phrase] = self.convert_html(self.cur_dst_phrase)

    """
    convert_html(txt='') -> str

    Make a text suitable for html rendering.

    txt = Text to parse.
    """
    def convert_html(self, txt=''):
        _txt = ''

        for c in txt:
            try:
                _txt += self.valid_chars[c]
            except:
                _txt += '&#' + str(ord(c)) + ';'

        return _txt

    """
    tr(phrase='') -> str

    Translate a phrase.

    phrase = ''
    """
    def tr(self, phrase=''):
        try:
            return self[phrase]
        except:
            return phrase
