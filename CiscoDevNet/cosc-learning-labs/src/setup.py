# from distutils.core import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
import os
import platform

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

from setuptools.command.test import test as TestCommand
import sys
class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

from setuptools import setup

if platform.system() == 'Windows':
    setup(
        name='cosc-learning-labs',
        description='Cisco Open SDN Controller (COSC) Learning Lab',
        version='1.0',
        packages=['basics', 'learning_lab', 'settings', ],
        url='http://github.com/CiscoDevNet/cosc-learning-labs',
        license='Apache License, Version 2.0',
        long_description=read('../README.md'),
        install_requires=[
            "requests",
            "ipaddress",
            "lxml",
            "logilab-common",
            "tabulate",
            "future",
        ],
        tests_require=['pytest','testfixtures'],
        cmdclass = {'test': PyTest},
    )
else:
        setup(
        name='cosc-learning-labs',
        description='Cisco Open SDN Controller (COSC) Learning Lab',
        version='1.0',
        packages=['basics', 'learning_lab', 'settings', ],
        url='http://github.com/CiscoDevNet/cosc-learning-labs',
        license='Apache License, Version 2.0',
        long_description=read('../README.md'),
        install_requires=[
            "requests",
            "ipaddress",
            "lxml",
            "logilab-common",
            "tabulate",
            "future",
            "pexpect",
        ],
        tests_require=['pytest','testfixtures'],
        cmdclass = {'test': PyTest},
    )