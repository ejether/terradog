
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




class meta(object):
    __version__ = "0.1.0"
    __author__ = 'Peak6 Technologies'
    __author_email__ = 'devops@peak6.com',



setup(name='terradog',
      version=meta.__version__,
      description='Peak6 Datadog Automation ',
      author=meta.__author__,
      author_email=meta.__author_email__,
      install_requires=[
           "click>=7.1.2,<8.0.0",
           "coloredlogs>=15.0,<16.0.0",
           "Jinja2==2.11.2",
           "ruyaml>=0.20.0,<0.21.0",
           "GitPython==3.1.11"
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
