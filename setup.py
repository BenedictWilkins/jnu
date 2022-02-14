#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Created on 29-01-2021 10:12:04

 [Description]
"""
__author__ ="Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ ="Development"


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 13:12:18 2019

@author: ben
"""

from setuptools import setup, find_packages

setup(name='jnu',
      version='0.0.1',
      description='',
      url='',
      author='Benedict Wilkins',
      author_email='benrjw@gmail.com',
      packages=find_packages(),
      install_requires=['jupyter', 'jupyterlab', 'ipykernel', 'ipython', 'ipywidgets', 'ipycanvas',
                        'scikit-image', 'matplotlib', 'scipy'],
      zip_safe=False)
