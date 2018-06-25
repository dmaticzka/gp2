#!/usr/bin/env python

import os
import sys
import subprocess
import re

from setuptools import setup
from setuptools.command.sdist import sdist as _sdist
from setuptools.command.install import install as _install

VERSION_PY = """
# This file is originally generated from Git information by running 'setup.py
# version'. Distribution tarballs contain a pre-generated copy of this file.

__version__ = '%s'
"""


def update_version_py():
    if not os.path.isdir(".git"):
        print("This does not appear to be a Git repository.")
        return
    try:
        p = subprocess.Popen(["git", "describe",
                              "--tags", "--always"],
                             stdout=subprocess.PIPE)
    except EnvironmentError:
        print("unable to run git, leaving gp2/_version.py alone")
        return
    stdout = p.communicate()[0]
    if p.returncode != 0:
        print("unable to run git, leaving gp2/_version.py alone")
        return
    ver = stdout.strip().decode()
    f = open("gp2/_version.py", "w")
    f.write(VERSION_PY % ver)
    f.close()
    print("set gp2/_version.py to '%s'" % ver)


def get_version():
    try:
        f = open("gp2/_version.py")
    except EnvironmentError:
        return None
    for line in f.readlines():
        mo = re.match("__version__ = '\D*(\d+[^']+)'", line)
        if mo:
            ver = mo.group(1)
            return ver
    return None


class sdist(_sdist):

    def run(self):
        update_version_py()
        self.distribution.metadata.version = get_version()
        return _sdist.run(self)


class install(_install):

    def run(self):
        _install.run(self)

    def checkProgramIsInstalled(self, program, args, where_to_download,
                                affected_tools):
        try:
            subprocess.Popen([program, args], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            return True
        except EnvironmentError:
            # handle file not found error.
            # the config file is installed in:
            msg = "\n**{0} not found. This " \
                  "program is needed for the following "\
                  "tools to work properly:\n"\
                  " {1}\n"\
                  "{0} can be downloaded from here:\n " \
                  " {2}\n".format(program, affected_tools,
                                  where_to_download)
            sys.stderr.write(msg)

        except Exception as e:
            sys.stderr.write("Error: {}".format(e))


setup(
    name='gp2',
    version=get_version(),
    author='Daniel Maticzka',
    author_email='maticzkd@informatik.uni-freiburg.de',
    packages=['gp2',
              ],
    scripts=[],
    include_package_data=True,
    package_data={},
    url='https://github.com/dmaticzka/gp2',
    license='LICENSE',
    description='gp2',
    long_description=open('README.md').read(),
    install_requires=[
        "eden >=3.0",
    ],
    cmdclass={'sdist': sdist, 'install': install}
)
