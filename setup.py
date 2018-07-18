#!/usr/bin/env python
# coding: utf-8
import os.path
import warnings
import sys
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

files_spec = [
    ('/etc/systemd/system/',['etc/systemd/system/syncthing-crypt.service','etc/systemd/system/syncthing-crypt@.service']),
    ('/etc/default/',['etc/default/syncthing-crypt'])
]
root = os.path.dirname(os.path.abspath(__file__))
data_files = []
for dirname, files in files_spec:
    resfiles = []
    for fn in files:
        if not os.path.exists(fn):
            raise IOError("File missing %s!"%fn)
        else:
            resfiles.append(fn)
    data_files.append((dirname, resfiles))

setuptools.setup(
    name="syncthing-crypt",
    version="0.0.1",
    author="t4skforce",
    author_email="7422037+t4skforce@users.noreply.github.com",
    description="Flask frontend for managing transparent encryption exposed over syncthing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/t4skforce/gocryptsyncthing",
    entry_points={'console_scripts': ['syncthing-crypt=syncthing_crypt:cli']},
    data_files=data_files,
    packages=setuptools.find_packages(),
    install_requires=[
        'Flask>=1.0.2',
        'Click>=6.7'
    ],
    python_requires='>=3',
    classifiers=(
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
