#!/usr/bin/env python
from setuptools import setup

from pathlib import Path

HERE = Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="python-cta",
    version="0.0.2",
    author="William Dean",
    author_email="wd60622@gmail.com",
    url="https://github.com/wd60622/cta",
    description="Python Client for Chicago Transit Data.",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["cta"],
    install_requires=["requests", "pandas"],
    test_require=["pytest", "pytest-mock"],
)
