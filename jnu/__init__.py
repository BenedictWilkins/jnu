#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Created on 29-01-2021 10:11:03

 [Description]
"""
__author__ ="Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ ="Development"

import os
import sys

import inspect
from inspect import getframeinfo
import io
from contextlib import redirect_stdout

from IPython.core.display import HTML
from IPython.display import display, clear_output

from . import image as jnu_image
from .image import hgallery 
from . import utils

import ipywidgets

@utils.normalise_input
def image(image, scale=1, show=True):
    image_widget = jnu_image.Image(image, scale=scale)
    if show:
        image_widget.display()
    return image_widget

@utils.normalise_input
def images(images, scale=1, on_interact=lambda x: None, step=0, value=0, show=True):
    image_widget = jnu_image.Image(images[step], scale=scale)
    
    # make it easy to display list meta data
    if hasattr(on_interact, '__getitem__'):
        l = on_interact
        def list_on_interact(z):
            print("value:", l[z]) #this only works with later version of ipython?
        on_interact = list_on_interact

    def slide(x):
        image_widget.update(images[x])
        on_interact(x)

    ipywidgets.interact(slide, x=ipywidgets.IntSlider(min=0, max=len(images)-1, step=step + 1, value=value, layout=dict(width='99%'))) #width 100% makes a scroll bar appear...?
    if show:
        image_widget.display()
    return image_widget

def progress(iterator, length=None, info=None):
    if info is not None:
        print(info)

    if length is None:
        try:
            length = len(iterator)
        except:
            print("Failed determine length of iterator, progress bar failed to display. Please provide the 'length' argument.")
            for i in iterator:
                yield i
            return

    f = ipywidgets.IntProgress(min=0, max=length, step=1, value=0) # instantiate the bar
    display(f)

    for i in iterator:
        yield i
        f.value += 1

def local_import(level=0):
    """ 
        Allow importing local .py files.
    """
    path = ".." + level * "/.."
    module_path = os.path.abspath(os.path.join(path))
    if module_path not in sys.path:
        sys.path.append(module_path)

def cell_variables():
    """ 
    Get all of the (global) variables in the current (or previous) Jupyter Notebook cell.

    Returns:
        dict: all global variables in the cell.
    """
    ipy = get_ipython()
    out = io.StringIO()
    
    with redirect_stdout(out): #get all cell inputs
        ipy.magic("history {0}".format(ipy.execution_count))
    cell_inputs = out.getvalue()
    
    #get caller globals ---- LOL HACKz
    frame = inspect.stack()[1][0]
    c_line = getframeinfo(frame).lineno
    g = frame.f_globals
    if not "_" in g:
        raise ValueError("The function \"cell_variables\" must be called from within a Jupyter Notebook.")
    
    IGNORE = "# ignore"
    #process each line...
    x = cell_inputs.replace(" ", "").split("\n")
    x.pop(c_line - 1) #lines are 1 indexed, remove the calling line 
    x = [a.split("=")[0] for a in x if "=" in a and IGNORE not in a] #all of the variables in the cell
    result = {k:g[k] for k in x if k in g}

    return result

