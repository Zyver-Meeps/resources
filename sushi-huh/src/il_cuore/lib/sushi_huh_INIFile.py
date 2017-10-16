#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_INIFile.py is part of Sushi, huh?.
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

# Module for manage INI type files.

import os

class INIFile(dict):
    def __init__(self, filename=''):
        self.load(filename)

    """
    load(filename='') -> None

    Load the INIFile file.

    filename = File to open.
    """
    def load(self, file_=''):
        try:
            if type(file_) == type(''):
                self.filename = file_
                ini_file = open(file_, 'rb')
            else:
                self.filename = file_.name
                ini_file = file_
        except:
            return

        try:
            data = ini_file.read()

            if type(data) == type(b''):
                data = data.decode()
        except:
            return

        ini_file.close()

        for line in data.split('\n'):
            line = line.replace('\r', '')
            line = line.strip()

            if line.find(';') != -1:
                line = line[: line.find(';')]

            if '[' in line:
                line = line.replace('[', '')
                line = line.replace(']', '')
                tag = line.strip()

                if not tag in self:
                    self[tag] = {}

                actual_tag = tag
            elif (line != ''):
                line = line.split('=')
                key = line[0].strip()

                values = []

                for value in line[1].split(','):
                    values += [value.strip().replace('%2C', ',')]

                self[actual_tag][key] = values

    """
    save() -> None

    Save the INIFile file.
    """
    def save(self):
        output = ''
        tags = sorted(self.keys())

        for tag in tags:
            output += '[' + tag + ']\n'
            longest = self.get_longest_size(self[tag])
            keys = []

            for key in self[tag]:
                _key  = key + (longest - len(key)) * ' ' + ' = '
                fst = True

                for value in self[tag][key]:
                    if fst == True:
                        fst = False
                    else:
                        _key += ', '

                    _key += str(value).replace(',', '%2C')

                _key += '\n'
                keys += [_key]

            for key in sorted(keys):
                output += key

            output += '\n'

        try:
            os.makedirs(os.path.dirname(self.filename))
        except:
            pass

        ini_file = open(self.filename, 'w')
        ini_file.write(output[: len(output) - 1])
        ini_file.close()

    """
    get_longest_size(keys={}) -> int

    Get the size of the longest word in keys, for stetic purposes.

    keys = Strings to compare.
    """
    def get_longest_size(self, keys={}):
        fst = True
        longest = 0

        for key in keys:
            if fst:
                longest = len(key)
                fst = False
            elif longest < len(key):
                longest = len(key)

        return longest

    """
    replace_keys(keys={}) -> None

    Replace the %(keyword)s by keys[keyword].

    keys = Keys to replace.
    """
    def replace_keys(self, keys={}):
        for tag in self:
            for key in self[tag]:
                for value in range(len(self[tag][key])):
                    for k in keys:
                        self[tag][key][value] = \
                        self[tag][key][value].replace('%(' + k + ')s', keys[k])

    """
    set_tag(tag='') -> None

    Set a tag in the INI file.

    tag = Tag to set.
    """
    def set_tag(self, tag=''):
        if not tag in self:
            self[tag] = {}

    """
    set_pair(tag='', key='', values=[]) -> None

    Set a pair (key, value) for a tag in the INI file.

    tag    = Tag to set
    key    = Key to set
    values = Values to set.
    """
    def set_pair(self, tag='', key='', values=[]):
        self.set_tag(tag)
        self[tag][key] = values

    """
    get_defaults() -> {}

    Get default values.
    """
    def get_defaults(self):
        defaults = {}

        for key in self['DEFAULT']:
            defaults[key] = self['DEFAULT'][key][0]

        return defaults
