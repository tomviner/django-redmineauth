#!/usr/bin/env python2

from setuptools import setup

setup(name='django-redmineauth',
    version='0.1',
    description='Login and automatically create Django superusers via Redmine login details. Based on django-acollabauth',
    author='Tom Viner',
    author_email='tom@viner.tv',
    packages=['redmineauth',],
)