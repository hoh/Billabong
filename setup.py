#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2014 "Hugo Herter http://hugoherter.com"
#
# This file is part of Billabong.
#
# Intercom is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup

setup(name='Billabong',
      version='0.2.1',
      description='Personal Encrypted file storage, backup and sharing',
      long_description=open('README.rst').read(),
      author='Hugo Herter',
      author_email='@hugoherter.com',
      url='https://github.com/hoh/Billabong/',
      packages=['billabong', 'billabong.storage'],
      install_requires=['pycrypto', 'python-magic', 'baker', 'paramiko'],
      license='AGPLv3',
      keywords="encrypted storage backup distributed",
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Programming Language :: Python :: 3',
                   'Intended Audience :: Developers',
                   'Intended Audience :: End Users/Desktop',
                   'Intended Audience :: Information Technology',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux',
                   'License :: OSI Approved :: GNU Affero General Public License v3',
                   'Topic :: Database',
                   'Topic :: Communications :: File Sharing',
                   'Topic :: Desktop Environment :: File Managers',
                   'Topic :: System :: Archiving :: Backup',
                   'Topic :: System :: Filesystems',
                   ],
      )
