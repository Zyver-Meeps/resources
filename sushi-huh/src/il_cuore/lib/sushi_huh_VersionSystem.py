#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_VersionSystem.py is part of Sushi, huh?.
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

# Version comparison tools.

class VersionSystem:
    """
    split_ver(string='')

    Convert a full version string in a vectorial format suitable for version comparison.

    string = The full version in natural string format.
    """
    def split_ver(self, string=''):
        if ':' in string:
            epoch, version = string.split(':', 1)
        else:
            epoch = ''
            version = string

        if '-' in version:
            upsver, debver = version.rsplit('-',1)
        else:
            upsver = version
            debver = ''

        return epoch, self.version2vector(upsver), self.version2vector(debver)

    """
    version2vector(version='')

    Convert a version string in a vectorial format suitable for version comparison.

    version = The version in natural string format.
    """
    def version2vector(self, version=''):
        vector = []
        digs = ''
        alps = ''

        for c in version:
            if c.isdigit():
                digs += c

                if alps != '':
                    vector += [alps]
                    alps = ''
            elif c.isalpha():
                alps += c

                if digs != '':
                    vector += [digs]
                    digs = ''
            else:
                if digs != '':
                    vector += [digs]
                    digs = ''

                if alps != '':
                    vector += [alps]
                    alps = ''

        if digs != '':
            vector += [digs]
            digs = ''

        if alps != '':
            vector += [alps]
            alps = ''

        return vector

    """
    normalize_vectors(vect1=[], vect2=[])

    Return two comparable strings from two vectors.

    vect1 = vector 1.
    vect2 = vector 2.
    """
    def normalize_vectors(self, vect1=[], vect2=[]):
        n_items = min([len(vect1), len(vect2)])
        normal_vect1 = ''
        normal_vect2 = ''

        for i in range(n_items):
            if (vect1[i].isdigit() and vect2[i].isalpha()) or (vect1[i].isalpha() and vect2[i].isdigit()):
                break

            l1 = len(vect1[i])
            l2 = len(vect2[i])
            max_item_len = max([l1, l2])
            difl1 = max_item_len - l1
            difl2 = max_item_len - l2

            if vect1[i].isdigit():
                normal_vect1 += difl1 * '0' + vect1[i]
            else:
                normal_vect1 += vect1[i] + difl1 * ' '

            if vect2[i].isdigit():
                normal_vect2 += difl2 * '0' + vect2[i]
            else:
                normal_vect2 += vect2[i] + difl2 * ' '

        return normal_vect1, normal_vect2

    """
    compare_versions(ver1='', comp='', ver2='')

    Return the result of the comparison between two versions.

    ver1 = Version string 1.
    comp = Type of comparison.
    ver2 = Version string 2.
    """
    def compare_versions(self, ver1='', comp='', ver2=''):
        res = False

        normal_vect1 = ''
        normal_vect2 = ''
        vect1 = self.split_ver(ver1)
        vect2 = self.split_ver(ver2)

        if vect1[0] != '' and vect2[0] != '':
            normal_epoch1, normal_epoch2 = self.normalize_vectors([vect1[0]], [vect2[0]])
            normal_vect1 += normal_epoch1
            normal_vect2 += normal_epoch2

        normal_ups1, normal_ups2 = self.normalize_vectors(vect1[1], vect2[1])
        normal_vect1 += normal_ups1
        normal_vect2 += normal_ups2

        if vect1[2] != [] and vect2[2] != []:
            normal_mant1, normal_mant2 = self.normalize_vectors(vect1[2], vect2[2])
            normal_vect1 += normal_mant1
            normal_vect2 += normal_mant2

        return eval('"{0}"{1}"{2}"'.format(normal_vect1, comp, normal_vect2))
