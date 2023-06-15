# -*- coding: utf-8 -*-

import os
from setuptools import setup


version = '0.0.1'


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-slack-oauth-simple',
    version=version,
    packages=[
        'django_slack_oauth_simple',
    ],
    include_package_data=True,
    license='MIT License',
    description='Handles OAuth and stores slack token',
    long_description=README,
    author='Marcelo Gumercino Costa',
    author_email='marcelogc@gmail.com',
    url='https://github.com/izdi/django-slack-oauth',
    download_url='https://github.com/izdi/django-slack-oauth/tarball/1.5.0',
    install_requires=[
        'Django>=1.8',
        'requests',
        'jsonfield',
    ],
)