#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from setuptools import setup, find_packages
from cascade_reveal import __version__
try:
    from pypandoc import convert
except ImportError:
    import io

    def convert(filename, fmt):
        with io.open(filename, encoding='utf-8') as fd:
            return fd.read()

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
]

setup(
    name='djangocms-cascade-reveal',
    version=__version__,
    description='Use Reveal.js in djangocms-cascade',
    author='Jacob Rief',
    author_email='jacob.rief@gmail.com',
    url='https://github.com/jrief/djangocms-cascade-reveal',
    packages=find_packages(),
    license='LICENSE-MIT',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    long_description=convert('README.md', 'rst'),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django-cms>=3.2.0',
        'djangocms-cascade>=0.7.3',
        'django-sass-processor>=0.3.4',
    ],
)
