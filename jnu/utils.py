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
  