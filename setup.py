#!/usr/bin/env python
from setuptools import setup, find_packages

try:
    from pyqt_distutils.build_ui import build_ui
    cmdclass = {'build_ui': build_ui}
except ImportError:
    cmdclass = {}


setup(
    name='Trustele',
    version='0.1',
    packages=find_packages(),
    license='Apache-2.0',
    author='Blockchainaire',
    author_email='blockchainaire@gmail.com',
    description='A Peer-to-Peer telegram operation tool',
    cmdclass=cmdclass,
)
