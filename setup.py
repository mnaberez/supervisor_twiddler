__version__ = '0.5-dev'

import os
import sys

if sys.version_info[:2] < (2, 4) or sys.version_info[0] > 2:
    msg = ("supervisor_twiddler requires Python 2.4 or later but does not "
           "work on any version of Python 3.  You are using version %s.  "
           "Please install using a supported version." % sys.version)
    sys.stderr.write(msg)
    sys.exit(1)

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
    package_dir = {'':'src'},
    packages = find_packages(os.path.join(here, 'src')),
    # put data files in egg 'doc' dir
    data_files=[ ('doc', [
        'CHANGES.txt',
        'LICENSE.txt',
        'README.md',
        ]
    )],
    install_requires = ['supervisor >= 3.0a10'],
    include_package_data = True,
    zip_safe = False,
    namespace_packages = ['supervisor_twiddler'],
    test_suite = 'supervisor_twiddler.tests'
)
