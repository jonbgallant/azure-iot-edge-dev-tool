#!/usr/bin/env python

import atexit
from subprocess import check_call

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install


with open('CHANGELOG.md') as history_file:
    history = history_file.read()

requirements = [
    'click>=6.0',
    'bcrypt<=3.1.7',
    'docker >= 3.7.0, <= 4.4.1',
    'python-dotenv',
    'requests >= 2.20.0, <= 2.25.1',
    'fstrings',
    'azure-cli-core',
    'azure-cli-iot',
    'azure-cli-profile',
    'azure-cli-extension',
    'azure-cli-configure',
    'azure-cli-resource',
    'azure-cli-cloud',
    'iotedgehubdev >= 0.14.3',
    'applicationinsights == 0.11.9',
    'commentjson == 0.9.0',
    'pyyaml>=4.1,<=4.2b4',
    'pypiwin32==219; sys_platform == "win32" and python_version < "3.6"',
    'pypiwin32==223; sys_platform == "win32" and python_version >= "3.6"',
    'more-itertools < 8.1.0'
]

setup_requirements = [
]

test_requirements = [
]


setup(
    name='iotedgedev',
    version='3.1.0rc1',
    description='The Azure IoT Edge Dev Tool greatly simplifies the IoT Edge development process by automating many routine manual tasks, such as building, deploying, pushing modules and configuring the IoT Edge Runtime.',
    long_description='See https://github.com/azure/iotedgedev for usage instructions.',
    author='Microsoft Corporation',
    author_email='vsciet@microsoft.com',
    url='https://github.com/azure/iotedgedev',
    packages=find_packages(include=['iotedgedev']),
    entry_points={
        'console_scripts': [
            'iotedgedev=iotedgedev.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license='MIT license',
    zip_safe=False,
    keywords='azure iot edge dev tool',
    python_requires='>=3.6, <3.8',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements
)
