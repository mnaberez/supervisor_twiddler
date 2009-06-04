__version__ = '0.3'

from ez_setup import use_setuptools
use_setuptools()

import os
import sys

if sys.version_info[:2] < (2, 3):
    msg = ("Py65 requires Python 2.4 or better, you are attempting to "
           "install it using version %s. Please install with a "
           "supported version" % sys.version)
    sys.stderr.write(msg)
    sys.exit(1)

from setuptools import setup, find_packages
here = os.path.abspath(os.path.dirname(__file__))

DESC = """\
supervisor_twiddler is an RPC extension for the supervisor2 package that
facilitates manipulation of supervisor's configuration and state in ways 
that are not normally accessible at runtime."""

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
    url = 'http://maintainable.com/software/supervisor_twiddler',
    description = "supervisor_twiddler RPC extension for supervisor2",
    long_description= DESC,
    classifiers = CLASSIFIERS,
    author = "Mike Naberezny",
    author_email = "mike@maintainable.com",
    maintainer = "Mike Naberezny",
    maintainer_email = "mike@maintainable.com",
    package_dir = {'':'src'},
    packages = find_packages(os.path.join(here, 'src')),
    install_requires = ['supervisor>=3.0a3'],
    include_package_data = True,
    zip_safe = False,
    namespace_packages = ['supervisor_twiddler'],
    test_suite = 'supervisor_twiddler.tests'
)
