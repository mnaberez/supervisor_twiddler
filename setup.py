__version__ = '1.0.0'

import os
import sys

py_version = sys.version_info[:2]

if py_version < (2, 6):
    raise RuntimeError(
        'On Python 2, supervisor_twiddler requires Python 2.6 or later')
elif (3, 0) < py_version < (3, 2):
    raise RuntimeError(
        'On Python 3, supervisor_twiddler requires Python 3.2 or later')

from setuptools import setup, find_packages
here = os.path.abspath(os.path.dirname(__file__))

DESC = """\
supervisor_twiddler is an RPC extension for Supervisor that allows
Supervisor's configuration and state to be manipulated in ways that are not
normally possible at runtime."""

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: No Input/Output (Daemon)',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Topic :: System :: Boot',
    'Topic :: System :: Systems Administration',
    ]

setup(
    name = 'supervisor_twiddler',
    version = __version__,
    license = 'License :: OSI Approved :: BSD License',
    url = 'http://github.com/mnaberez/supervisor_twiddler',
    description = "supervisor_twiddler RPC extension for Supervisor",
    long_description= DESC,
    classifiers = CLASSIFIERS,
    author = "Mike Naberezny",
    author_email = "mike@naberezny.com",
    maintainer = "Mike Naberezny",
    maintainer_email = "mike@naberezny.com",
    packages = find_packages(),
    install_requires = ['supervisor >= 3.0a10'],
    include_package_data = True,
    zip_safe = False,
    namespace_packages = ['supervisor_twiddler'],
    test_suite = 'supervisor_twiddler.tests'
)
