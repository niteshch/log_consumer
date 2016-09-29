#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='monitor',
    version='1.0.1',
    description='Parse log files, generate metrics for Graphite and Ganglia',
    packages=[
        'logster',
        'logster/parsers',
        'logster/tailers',
        'logster/outputs'
    ],
    install_requires = [
        'pygtail>=0.5.1'
    ],
    zip_safe=False,
    scripts=[
        'monitor'
    ],
    license='GPL3',
)
