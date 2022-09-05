#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Setup script."""

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    # remove header
    header_lines = 3
    long_description = long_description.split("\n", header_lines)[header_lines]

project_urls = {
    'Documentation': "https://github.com/bakobako/kcf-tools"
}

setup(
    name='kcf-tools',
    version='0.1.2',
    description="CLI tools for generating documentation and config schemas for Keboola Component development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls=project_urls,
    author="Adam Bako @bakobako",
    author_email='adam.bako@keboola.com',
    url='https://github.com/bakobako/kcf-tools',
    packages=find_packages(),
    package_data={'': ['*.md']},
    package_dir={
        'kcf_tools': 'kcf_tools'
    },
    entry_points={
        'console_scripts': [
            'kcf-tools=kcf_tools.cli:main'
        ]
    },
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=[
        'click',
        'Jinja2==3.1.1',
        'prompt_toolkit==1.0.14',
        'PyInquirer==1.0.3',
        'Pygments==2.11.2'
    ],
    zip_safe=False,
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
