#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="clipboard-actions",
    version="0.9",
    packages=find_packages(),
    py_modules=[],
    entry_points={
        'console_scripts': [
            'clipboard-actions = clipboard_actions.__main__:main',
        ],
    },
)
