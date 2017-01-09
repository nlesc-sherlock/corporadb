#!/usr/bin/env python
# SIM-CITY client
#
# Copyright 2015 Netherlands eScience Center <info@esciencecenter.nl>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    from setuptools import setup
    from setuptools.command.build_ext import build_ext as _build_ext
except ImportError:
    from distutils.core import setup

from pip.req import parse_requirements
from pip.download import PipSession

instreqs = parse_requirements('requirements.txt',session = PipSession())
reqs = [str(ir.req) for ir in instreqs]

setup(name = 'corpora',
      version = '0.1',
      description = 'Topic models for a corpus of text.',
      author = 'Carlos Martinez Ortiz',
      author_email = 'c.martinez@esciencecenter.nl',
      url = 'https://github.com/nlesc-sherlock/corporadb',
      packages = ['corpora'],
      scripts =
      ['corpora/cleanHeaders.py','corpora/tokenization.py','corpora/buildDict.py','corpora/buildDocumentMatrix.py'],
      classifiers = [
          'License :: OSI Approved :: Apache Software License',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Environment :: Console',
          'Development Status :: 2 - Pre-Alpha',
          'Natural Language :: English',
          'Operating System :: POSIX :: Linux',
          'Operating System :: MacOS :: MacOS X',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Text Processing :: Linguistic',
      ],
      setup_requires = ['numpy'],
      install_requires = reqs)

