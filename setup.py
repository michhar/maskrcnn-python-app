#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: setup.py
Description: Setup script to build and distribute maskrcnn module.
"""

import io

from setuptools import find_packages
from setuptools import setup

README = 'README.md'


def readme():
    """Parse README for long_description."""
    return io.open(README, encoding='utf-8').read()

setup(
    name='maskrcnn-detect',
    version='0.0.9',
    packages=find_packages(exclude=['tests']),
    install_requires=['requests',
                      'tensorflow==2.6.2',
                      'cython',
                      'h5py',
                      'scikit-image',
                      'opencv-python',
                      'matplotlib',
                      'jupyter',
                      'imgaug'],
    author='Micheleen Harris',
    description='Python SDK for the MaskRCNN projects',
    long_description=readme(),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/maskrcnn-python-app',
    classifiers=[
        'Development Status :: 5 - Development/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Instance Segmentation',
    ],
    test_suite='nose.collector',
    tests_require=['nose'])
