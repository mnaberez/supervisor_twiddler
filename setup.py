__version__ = '1.1.0-dev'

import os
import sys

py_version = sys.version_info[:2]

if py_version < (2, 7):
    raise RuntimeError(
        'On Python 2, supervisor_twiddler requires Python 2.7 or later')
elif (3, 0) < py_version < (3, 2):
    raise RuntimeError(
        'On Python 3, supervisor_twiddler requires Python 3.2 or later')

tests_require = []
if py_version < (3, 3):
    tests_require.append('mock<4.0.0.dev0')

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
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
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
    tests_require = tests_require,
    include_package_data = True,
    zip_safe = False,
    namespace_packages = ['supervisor_twiddler'],
    test_suite = 'supervisor_twiddler.tests'
)
