# -*- coding: utf-8 -*-

#!/usr/bin/env python

from setuptools import setup

setup(
    name='easyimpress',
    version='0.1',
    description='Slides generation from markdown to impress.js',
    author='Álex González',
    author_email='agonzalezro@gmail.com',
    url='http://github.com/agonzalezro/easyimpress',
    packages=['easyimpress'],
    install_requires=[
        'jinja2',
        'markdown2'
    ])
