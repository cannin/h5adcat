#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import io
import re
import os
from setuptools import find_packages, setup

DEPENDENCIES = ['scanpy==1.9.1']
EXCLUDE_FROM_PACKAGES = ["contrib", "docs", "test*"]
CURDIR = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(CURDIR, "README.md"), "r", encoding="utf-8") as f:
    README = f.read()


def get_version():
    main_file = os.path.join(CURDIR, "h5adcat", "main.py")
    _version_re = re.compile(r"__version__\s+=\s+(?P<version>.*)")
    with open(main_file, "r", encoding="utf8") as f:
        match = _version_re.search(f.read())
        version = match.group("version") if match is not None else '"unknown"'
    return str(ast.literal_eval(version))


setup(
    name="h5adcat",
    version=get_version(),
    author="TBA",
    author_email="TBA",
    description="",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/cannin/TBA",
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    keywords=[],
    scripts=[],
    entry_points={"console_scripts": ["h5adcat=h5adcat:main"]},
    zip_safe=False,
    install_requires=DEPENDENCIES,
    #test_suite="tests.test_project",
    python_requires=">=3.7",
    # license and classifier list:
    # https://pypi.org/pypi?%3Aaction=list_classifiers
    license="License :: OSI Approved :: Apache Software License",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
        # "Private :: Do Not Upload"
    ],
)