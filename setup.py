#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Setup script."""

from setuptools import setup

with open('requirements.txt') as req_file:
    requirements = req_file.read().splitlines()

setup(
    name='kcf-tools',
    version='0.0.1',
    description="CLI tools for generating documentation and config schemas for Keboola Component development",
    long_description="readme",
    long_description_content_type="text/markdown",
    author="Adam Bako @bakobako",
    author_email='adam.bako@keboola.com',
    url='https://github.com/bakobako/kcf-tools',
    packages=["kcf_tools"],
    package_dir={
        'kcf_tools': 'kcf_tools'
    },
    entry_points={
        'console_scripts': [
            'kcf_tools=kcf_tools.cli:main'
        ]
    },
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=requirements,
    zip_safe=False,
    keywords='obs-img-utils obs_img_utils',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ]
)