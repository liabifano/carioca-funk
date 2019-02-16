#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='carioca-funk',
      url='',
      author='',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      version='0.0.1',
      install_requires=[
          'numpy==1.15.1',
          'pytest==3.7.4',
          "Scrapy==1.6.0",
      ],
      include_package_data=True,
      zip_safe=False)
