#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sushi, huh? offline package downloader for GNU/Linux systems
# Copyright (C) 2008  Gonzalo Exequiel Pedone
#
# sushi_huh_PackagesDB.py is part of Sushi, huh?.
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

# Packages database manager module.

import sys
import os
import pickle
import tempfile
import zipfile

from sushi_huh_Commons import Commons
from sushi_huh_VersionSystem import VersionSystem
from sushi_huh_Table import Table
from sushi_huh_INIFile import INIFile

class PackagesDB:
    def __init__(self):
        self.version_system = VersionSystem()
        self.commons = Commons()
        self.first_time_run = not os.path.exists(self.commons['packages_db'])
        self.packages_db = self.commons.get_temp(''.join([os.path.splitext(self.commons['packages_db'])[0], '.db']))

        if self.first_time_run:
            if os.path.exists(self.packages_db):
                os.remove(self.packages_db)
        else:
            # Uncompress the database in the temporal directory.
            if not os.path.exists(self.packages_db):
                packages_zip = zipfile.ZipFile(self.commons['packages_db'])
                packages_zip.extractall(tempfile.gettempdir())
                packages_zip.close()

        self.local_packages = []
        self.local_provides = {}
        self.downloaded_packages = []

        try:
            self.local_packages, self.local_provides = pickle.load(open(os.path.join(self.commons['settings_path'], 'provides.db'), 'rb'))
        except:
            pass

        self.update_downloades()

        self.packages_cols = ['package_id', 'name', 'version', 'release', 'arch', 'groupname', 'gui', 'repository', 'size', 'summary', 'description', 'url', 'path', 'status']
        self.packages = Table(self.packages_cols)

        self.requires = {}
        self.provides = {}

        if not self.first_time_run:
            # Load the database.
            self.packages.table, self.packages.sorted_by, self.requires, self.provides = pickle.load(open(self.packages_db, 'rb'))

    """
    update_downloades()

    Collect information about downloades packages.
    """
    def update_downloades(self):
        try:
            downloads_ini_file = INIFile(os.path.join(self.commons['settings_path'], 'downloads.ini'))
            self.downloaded_packages = [filename[filename.rfind('/') + 1:] for filename in downloads_ini_file['files'].keys()]
        except:
            self.downloaded_packages = []

    """
    make_sync()

    Determine the status of the packages.
    """
    def make_sync(self):
        self.update_downloades()
        sync_table = []

        for package in self.packages.table:
            filename = self.get_filename(package)

            if filename in self.local_packages:
                package[13] = 2
            elif filename in self.downloaded_packages:
                package[13] = 1
            else:
                package[13] = 0

            sync_table += [package]

        self.packages.table = sync_table
        self.commit()

    """
    get_filename(full_filename='')

    Return a filename with out the path.

    full_filename = Full path.
    """
    def get_filename(self, full_filename=''):
        return full_filename[0][full_filename[0].rfind('/') + 1:]

    """
    close()

    Close the packages database.
    """
    def close(self):
        if self.first_time_run:
            self.commit()

        os.remove(self.packages_db)

    """
    commit()

    Save the changes to the data base.
    """
    def commit(self):
        # Dump all information to a file using the Python 3 binary file format.
        pickle.dump((self.packages.table, self.packages.sorted_by, self.requires, self.provides), open(self.packages_db, 'wb'))

        # Compress the database in a zip file.
        packages_zip = zipfile.ZipFile(self.commons['packages_db'], 'w', zipfile.ZIP_DEFLATED)
        packages_zip.write(self.packages_db, ''.join([os.path.splitext(os.path.basename(self.commons['packages_db']))[0], '.db']))
        packages_zip.close()

    """
    get_groups() -> []

    Returns all available packages groups.
    """
    def get_groups(self):
        groupname_index = self.packages.cols.index('groupname')

        return sorted(set(row[groupname_index] for row in self.packages.table))

    """
    get_description(package_id='') -> []

    Returns a full information about the requested package.

    package_id = Package id.
    """
    def get_description(self, package_id=''):
        return self.packages.find_exact(package_id, 'package_id').table[0]

    """
    get_packages(groupname='') -> []

    Returns a list of packages sorted by name where "groupname" column is
    equal to groupname.

    groupname = Group name.
    """
    def get_packages(self, groupname=''):
        return self.packages.find_exact(groupname, 'groupname', 'name').table

    """
    search(require=[], keywords=[]) -> []

    Returns a list of packages sorted by name containing the keywords in "name",
    "summary" or "description" columns.

    keywords = Keywords to search.
    """
    def search(self, keywords=[]):
        return self.packages.find_contains(keywords, ['name', 'summary', 'description'], 'name').table

    """
    carry_out_dependency(require=[], provide=[]) -> bool

    Returns True if the provide is compatible with the require.

    require = [name, flag, version].
    provide = [name, flag, version]
    """
    def carry_out_dependency(self, require=[], provide=[]):
        # !s+sc
        return require[1] == '' or (require[1] != '' and self.version_system.compare_versions(provide[1], require[1], require[2]))

    """
    get_dependencies(packages=[], suggests_are_requires=False) -> []

    Return a full list of the packages dependencies id that you must download for install the needed
    packages.

    filenames             = List of packages id.
    suggests_are_requires = Also download the suggested packages
    """
    def get_dependencies(self, packages=[], suggests_are_requires=False):
        old_requires = []
        new_requires = []
        old_packages = set()
        new_packages = set(packages)
        total_size = 0

        # For each package in new_packages.
        while new_packages != set():
            package_id = new_packages.pop()
            old_packages.add(package_id)

            try:
                package_info = self.requires[package_id]
                total_size += package_info[0]

                # Find all their requires.
                for require in package_info[1]:
                    if not require in old_requires:
                        new_requires += [require]

                # Y nessesary, also find all their suggest:
                if suggests_are_requires:
                    for suggest in package_info[2]:
                        if not suggest in old_requires:
                            new_requires += [suggest]
            except:
                pass

            # Now find all packages that provides each require.
            while new_requires != []:
                require = new_requires.pop()
                old_requires += [require]

                if not self.in_local_provides(require):
                    try:
                        provides = self.provides[require[0]]
                    except:
                        provides = []

                    # Append valid packages to new_packages.
                    for provide in provides:
                        if self.carry_out_dependency(require, provide):
                            if not provide[2] in old_packages and not self.get_filename(provide[2]) in self.downloaded_packages:
                                new_packages.add(provide[2])

        return sorted(old_packages), total_size

    def in_local_provides(self, dependency):
        try:
            return self.carry_out_dependency(dependency, [dependency[0], '==', self.local_provides[dependency[0]]])
        except:
            return False

    """
    resolve_files(packages=[]) -> {}

    Returns {full_local_path: [full_download_url, pacakge_size]}

    packages = List of packages id.
    """
    def resolve_files(self, packages=[]):
        url_index = self.packages_cols.index('url')
        path_index = self.packages_cols.index('path')
        size_index = self.packages_cols.index('size')

        files = {}

        for package in set(packages):
            try:
                pkg_info = self.get_description(package)
                files[pkg_info[path_index]] = [pkg_info[url_index], pkg_info[size_index]]
            except:
                pass

        return files
