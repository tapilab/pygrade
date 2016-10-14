#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

# read requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

test_requirements = requirements
#[
#    # TODO: put package test requirements here
#    'nose'
#]

setup(
    name='pygrade',
    version='0.2.3',
    description="auto-grade python assignments",
    long_description=readme + '\n\n' + history,
    author="Aron Culotta",
    author_email='aronwc@gmail.com',
    url='https://github.com/tapilab/pygrade',
    packages=[
        'pygrade',
    ],
    package_data={'pygrade': ['requirements.txt']},
    package_dir={'pygrade':
                 'pygrade'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='pygrade',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        'console_scripts': [
            'pygrade = pygrade.pygrade:main',
            'pygrade-cheat = pygrade.cheat:main',
            'pygrade-clone = pygrade.clone:main',
            'pygrade-grade = pygrade.grade:main',
            'pygrade-init = pygrade.init:main',
            'pygrade-push = pygrade.push:main',
            'pygrade-summarize = pygrade.summarize:main',
        ],
    },
    test_suite='tests',
    tests_require=test_requirements
)
