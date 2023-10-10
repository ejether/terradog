#!/usr/bin/env python
import sys

try:
    from distutils.errors import DistutilsSetupError
    from setuptools import setup, find_packages
    from setuptools.command.install import install
except ImportError:
    print("setup tools required. Please run: "
          "pip install setuptools).")
    sys.exit(1)

setup(name='terradog',
      use_scm_version=True,
      setup_requires=['setuptools_scm'],
      description='Peak6 Datadog Automation',
      author='Peak6 Technologies',
      author_email='devops@peak6.com',
      install_requires=[
           "click>=7.1.2,<8.0.0",
           "coloredlogs>=15.0,<16.0.0",
           "Jinja2==2.11.3",
           "ruyaml>=0.20.0,<0.21.0",
           "GitPython==3.1.37"
      ],
      packages=find_packages(
          exclude=['tests']),
      include_package_data=True,
      entry_points=''' #for click integration
          [console_scripts]
          terradog=terradog.cli:cli
      ''',
      python_requires=">=3.9"
      )
