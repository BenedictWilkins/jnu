#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Created on 29-01-2021 14:29:48

 [Description]
"""
__author__ ="Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ ="Development"

import numpy as np

# DECORATORS

def as_numpy(fun): # TODO this could be made nicer? by providing the arguments to check/convert...
    try: # convert torch arguments to numpy if torch is in use

        import torch
        def to_numpy(*args, **kwargs):           
            def _to_numpy(x):
                if torch.is_tensor(x):
                    return x.detach().cpu().numpy()
                else:
                    return x
            return fun(*[_to_numpy(a) for a in args], **{k:_to_numpy(v) for k,v in kwargs.items()})
        
        return to_numpy

    except:
        return fun # torch is not in use
    
def as_HWC(*indx): # converts an the arguments given to HWC [0-255] image format
    """ Yo dawg I heard you like closures... """

    def decorator(fun):

        def wrapper(*args, **kwargs):

            def convert(image):
                if len(image.shape) == 2: 
                    image = image[...,np.newaxis]

                assert len(image.shape) in [3,4] # (N)HWC or (N)CHW format
                C = len(image.shape) - 3

            
                if image.shape[C] in [3,1] and not image.shape[-1] in [3,1]: # we are in CHW format, convert to HWC
                    axis = tuple([0] * C + [1 + C, 2 + C, 0 + C])
                    image = image.transpose(axis)
  
                assert image.shape[-1] in [3, 1]

                if issubclass(image.dtype.type, np.floating): # convert to 0-255 range
                    image = image * 255 # assume [0-1] ... 
                
                image = image.astype(np.uint8)
   
                #if image.shape[-1] == 1: # convert to 3 channel image
                #   image = np.repeat(image, 3, axis=-1)

                return image

            args = list(args)
            for i in indx:
                args[i] = convert(args[i])

            return fun(*args, **kwargs)
                    
        return wrapper
        
    return decorator