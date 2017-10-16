#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_PyHP.py is part of Sushi, huh?.
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

# Parser for Python code in HTML files.

try:
    import StringIO
except:
    import io as StringIO

import sys
import tempfile
import traceback

from sushi_huh_Commons import Commons

class PyHP:
    """
    __init__(filename='', content='', **shared_var)

    filename = File to parse.
    content = If a filename is not provided then PyHP will parse this variable.
    shared_var = Shared variables.
    """
    def __init__(self, filename='', content='', **shared_var):
        try:
            if filename == '':
                raw_html = content
            else:
                f = open(filename, 'r')
                raw_html = f.read()
                f.close()
        except:
            old_stderr = sys.stderr
            sys.stderr = StringIO.StringIO()
            type_, value, traceback_ = sys.exc_info()
            traceback.print_exception(type_, value, traceback_)
            sys.stderr.seek(0)
            error = sys.stderr.read()
            sys.stderr.close()
            sys.stderr = old_stderr
            self.html = self.error_msg_to_html(error)

            return

        commons = Commons()
        raw_html_copy = raw_html[:]
        pycodes = {}
        pycodes_list = []

        # Reads all code pieces...
        python_head = '<?pyhp'
        python_tail = '?>'
        match_head = raw_html_copy.find(python_head)

        while match_head != -1:
            match_tail = raw_html_copy.find(python_tail)
            code_from = code_to = raw_html_copy[match_head + len(python_head): match_tail]
            code_from = ''.join([python_head, code_from, python_tail])
            pycodes[code_from] = code_to.strip()
            pycodes_list += [code_from]
            raw_html_copy = raw_html_copy[match_tail + len(python_tail):]
            match_head = raw_html_copy.find(python_head)

        python_script = ''

        #  and join all code pieces with a print('<?pyhpout?>') instruction in a single code piece.
        for pycode in pycodes_list:
            python_script += 'print(\'<?pyhpout?>\')\n' + pycodes[pycode] + '\n'

        old_stdout = sys.stdout
        sys.stdout = StringIO.StringIO()

        error = ''

        # Executes the code.
        try:
            exec(python_script, globals(), locals())
        except:
            old_stderr = sys.stderr
            sys.stderr = StringIO.StringIO()
            type_, value, traceback_ = sys.exc_info()
            traceback.print_exception(type_, value, traceback_)
            sys.stderr.seek(0)
            error = sys.stderr.read()
            sys.stderr.close()
            sys.stderr = old_stderr

        sys.stdout.seek(0)
        output = sys.stdout.read()
        sys.stdout.close()
        sys.stdout = old_stdout

        if error != '':
            self.html = self.error_msg_to_html(error)

            return

        # Obtains the output for each piece of code.
        outputs = output.split('<?pyhpout?>\n')
        del outputs[0]

        n_code = 0

        # Replace the pieces of code with they output.
        for output in outputs:
            pycodes[pycodes_list[n_code]] = output[: len(output) - 1]
            n_code += 1

        self.html = raw_html

        for pycode in pycodes:
            self.html = self.html.replace(pycode,  pycodes[pycode])

    """
    error_msg_to_html(error='') -> None

    Convert a error string in a valid HTML string.

    error = Error message.
    """
    def error_msg_to_html(self, error=''):
        return '<DIV class = "ui-state-error ui-corner-all" style = "width: 100%; height: 100%; overflow: auto">' + '<BR>\n'.join(error.replace('&', '&amp;').replace(' ', '&nbsp;').replace('<', '&lt;').replace('>', '&gt;').split('\n')) + '</DIV>'
