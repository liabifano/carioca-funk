#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='carioca_funk',
      url='',
      author='',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      version='0.0.1',
      install_requires=[
          'numpy==1.15.1',
          'pytest==3.7.4',
          'Scrapy==1.6.0',
          'jedi==0.13.2',
          'rope==0.11.0',
          'autopep8==1.4',
          'yapf==0.23.0',
          'flake8==3.7.6',
          'epc==0.0.5',
          'pandas==0.23.0',
          "nltk==3.4.5",
      ],
      include_package_data=True,
      zip_safe=False)
