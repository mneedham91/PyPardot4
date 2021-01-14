#!/usr/bin/env python
from setuptools import setup

VERSION = "0.1.0"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="PyPardotSF",
    version=VERSION,
    description="API wrapper for API v3 & v4 of Pardot marketing automation software.",
    keywords="pardot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Daigo Tanaka, Anelen Co., LLC",
    url="https://github.com/anelendata/PyPardotSF",

    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",

        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",

        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],

    install_requires=['requests'],

    packages=["pypardot", "pypardot.objects", "pypardot.objects_v3"],
    package_data={
        # Use MANIFEST.ini
    },
    include_package_data=True
)
