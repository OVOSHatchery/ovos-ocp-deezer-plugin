#!/usr/bin/env python3
import os
from setuptools import setup, find_packages

BASEDIR = os.path.abspath(os.path.dirname(__file__))

### replace this data with your plugin specific info
PLUGIN_TYPE = "ovos.ocp.extractor"
PLUGIN_NAME = 'ovos-ocp-deezer-plugin'
PLUGIN_PKG = PLUGIN_NAME.replace("-", "_")
PLUGIN_CLAZZ = "OCPDeezerExtractor"
PLUGIN_CONFIGS = f"{PLUGIN_CLAZZ}Config"
###

PLUGIN_ENTRY_POINT = f'{PLUGIN_NAME} = {PLUGIN_PKG}:{PLUGIN_CLAZZ}'
CONFIG_ENTRY_POINT = f'{PLUGIN_NAME}.config = {PLUGIN_PKG}:{PLUGIN_CONFIGS}'


def get_version():
    """ Find the version of the package"""
    version = None
    version_file = os.path.join(BASEDIR, PLUGIN_PKG, 'version.py')
    major, minor, build, alpha = (None, None, None, None)
    with open(version_file) as f:
        for line in f:
            if 'VERSION_MAJOR' in line:
                major = line.split('=')[1].strip()
            elif 'VERSION_MINOR' in line:
                minor = line.split('=')[1].strip()
            elif 'VERSION_BUILD' in line:
                build = line.split('=')[1].strip()
            elif 'VERSION_ALPHA' in line:
                alpha = line.split('=')[1].strip()

            if ((major and minor and build and alpha) or
                    '# END_VERSION_BLOCK' in line):
                break
    version = f"{major}.{minor}.{build}"
    if alpha and int(alpha) > 0:
        version += f"a{alpha}"
    return version


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    with open(os.path.join(BASEDIR, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        if 'MYCROFT_LOOSE_REQUIREMENTS' in os.environ:
            print('USING LOOSE REQUIREMENTS!')
            requirements = [r.replace('==', '>=').replace('~=', '>=') for r in requirements]
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]


setup(
    name=PLUGIN_NAME,
    version=get_version(),
    description='OCP youtube stream extractor plugin',
    url=f'https://github.com/OpenVoiceOS/{PLUGIN_NAME}',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    packages=find_packages(include=[f'{PLUGIN_PKG}*']),
    install_requires=required("requirements.txt"),
    zip_safe=True,
    include_package_data=True,
    keywords='ovos ocp plugin',
    entry_points={PLUGIN_TYPE: PLUGIN_ENTRY_POINT,
                  f'{PLUGIN_TYPE}.config': CONFIG_ENTRY_POINT}
)
