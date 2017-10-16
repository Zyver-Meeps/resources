#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_Table.py is part of Sushi, huh?.
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

# Provides various functions for work with tables.

import sys

class Table():
    """
    __init__(cols=[])

    cols = List of columns names of the table.
    """
    def __init__(self, cols=[]):
        self.cols = cols
        self.table = []
        self.sorted_by = None

    """
    sort_table(col=None) -> None

    Sort the table by column name.

    col = Column name.
    """
    def sort_table(self, col=None):
        if col == None or self.sorted_by == col or self.table == []:
            return

        col_index = self.cols.index(col)
        self.table = sorted([row[col_index]] + row[: col_index] + row[col_index + 1:] for row in self.table)
        self.table = [row[1: col_index + 1] + [row[0]] + row[col_index + 1:] for row in self.table]
        self.sorted_by = col

    """
    find_exact(keyword='', col='', sort_by=None) -> Table()

    Search a keyword.

    keyword = Keyword to search.
    col = Search in column.
    sort_by = Sort results by columns.
    """
    def find_exact(self, keyword='', col='', sort_by=None):
        filter_table = Table(self.cols)

        self.sort_table(col)
        col_index = self.cols.index(col)
        ftable = [row[col_index] for row in self.table]

        try:
            low = ftable.index(keyword)
            ftable.reverse()
            hi = len(ftable) - ftable.index(keyword)
            filter_table.table = self.table[low: hi]
        except:
            filter_table.table = []

        filter_table.sort_table(sort_by)

        return filter_table

    """
    find_contains(keywords=[], cols=[], sort_by=None) -> Table()

    Search a keyword.

    keyword = Keyword to search.
    col = Search in column.
    sort_by = Sort results by columns.
    """
    def find_contains(self, keywords=[], cols=[], sort_by=None):
        filter_table = Table(self.cols)
        cols = [self.cols.index(col) for col in cols]
        keywords = [keyword.lower() for keyword in keywords]

        for row in self.table:
            r = str([row[col] for col in cols]).lower()

            for keyword in keywords:
                if keyword in r:
                    filter_table.table += [row]
                    break

        filter_table.sort_table(sort_by)

        return filter_table
