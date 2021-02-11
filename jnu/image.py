#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Created on 29-01-2021 10:54:08

 [Description]
"""
__author__ ="Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ ="Development"

import numpy as np

#mport plotly.offline as pyo
#import plotly.graph_objs as go
#import plotly.figure_factory as ff
# Set notebook mode to work in offline
#pyo.init_notebook_mode()

from IPython.display import display, clear_output

#from ipyevents import Event 
from ipycanvas import Canvas, MultiCanvas

from matplotlib import pyplot as plt
from matplotlib import animation
from IPython.display import HTML

import ipywidgets
import skimage



from . import utils

@utils.as_numpy
def resize(image, size):
    return skimage.transform.resize(image, size, order=0, preserve_range=True)

@utils.as_numpy
def HWC(image):
    if len(image.shape) == 2:
        return image[:,:,np.newaxis]

    C_index = len(image.shape) - 3
    if image.shape[C_index] in [3,1] and not image.shape[-1] in [3,1]: # we are in CHW format, convert to HWC
        if len(image.shape) == 3:    
            return image.transpose((1,2,0))
        elif len(image.shape) == 4:
            return image.transpose((0,2,3,1))

    assert image.shape[-1] in [1,3]

    return image # ready in HWC format

@utils.as_numpy
def hgallery(x, n=10):
    x = HWC(x)

    if n is None:
        n = x.shape[0]
    m,h,w,c = x.shape
    n = min(m, n) #if n is larger, just use m
    if m % n != 0:
        pad = ((0, n - (m % n)),*([(0,0)]*(len(x.shape)-1)))
        x = np.pad(x, pad)
        m,h,w,c = x.shape
    return x.swapaxes(1,2).reshape(m//n, w * n, h, c).swapaxes(1,2)

class Video:
    
    def __init__(self, video, frame_rate = 30, interpolation='nearest'):
        super(Video, self).__init__()

        self.video = video
        self.frame_rate = frame_rate

        if isinstance(video, str):
            raise NotImplementedError("TODO - play video from file")

        elif isinstance(video, np.ndarray):
            fig = plt.figure()
            im = plt.imshow(self.video[0,...], interpolation = interpolation)
            plt.axis('off')
            plt.close() 

            def init():
                im.set_data(self.video[0,:,:,:])

            def animate(i):
                im.set_data(self.video[i,:,:,:])
                return im

            anim = animation.FuncAnimation(fig, animate, init_func=init, frames=self.video.shape[0],
                                            interval=1000/self.frame_rate)

            self.fig = HTML(anim.to_html5_video())

    def display(self):
        display(self.fig)

class Image:

    def __init__(self, image, scale=1):
        self.scale = scale
        self.image = self.normalise(image)
    
        self.canvas = Canvas(width=self.image.shape[1], height=self.image.shape[0], scale=1)
        self.canvas.put_image_data(self.image, 0, 0) 
    
    def normalise(self, image):
        # convert image to the correct format for display in an ipycanvas

        if len(image.shape) == 2: 
            image = image[np.newaxis,...]
        assert len(image.shape) == 3 # HWC or CHW format

        if image.shape[0] in [3,1] and not image.shape[-1] in [3,1]: # we are in CHW format, convert to HWC
            image = image.transpose((1,2,0))
        
        assert image.shape[-1] in [3, 1]

        if issubclass(image.dtype.type, np.floating): # convert to 0-255 range
            image = image * 255 # assume [0-1] ... 

        image = image.astype(np.float32)

        if self.scale != 1: # scale image
            shape = list(image.shape)
            shape[0] *= self.scale
            shape[1] *= self.scale
            image = resize(image, shape)
        
        if image.shape[-1] == 1: # convert to 3 channel image
            image = np.repeat(image, 3, axis=-1)

        return image

    def update(self, image):
        image = self.normalise(image)
        assert image.shape == self.image.shape # shapes must be the same
        self.canvas.put_image_data(image, 0, 0) 

    def display(self): # TODO update
        box_layout = ipywidgets.Layout(display='flex',flex_flow='row',align_items='center',width='100%')
        display(ipywidgets.HBox([self.canvas], layout=box_layout))