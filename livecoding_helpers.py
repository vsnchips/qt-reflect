print ("Hello Dan's livecoding helpers")

import os
import sys
sys.path.append('.')

import numpy as np

import importlib as il

def preview(image):
    previewName(image,'Preview')

def previewName(image,name):
    import cv2
    cv2.namedWindow(name)
    cv2.imshow(name,image)
    cv2.waitKey(100)

import PyQt5

def execfile(file,globs):
    global __name__
    __name__='__mp_main__'
    script= open(file,'r').read()
    exec(script,globs,locals())
    
'''
if (__name__ == '__main__'):
    import sys
    import importlib as il
    il.invalidate_caches()
    mod=il.import_module(sys.argv[1])
    for thing in dir(mod):
        globals()[thing] = getattr(mod,thing)
    __name__ = 'live_interpreter'
'''

class mPatcher:
    @classmethod
    def m_patch(self,state,newdef):
        for k in newdef.__dict__:
            obj=getattr(newdef,k)
            if not k.startswith('_') and callable(obj):
                setattr(state, k, obj)
patch=mPatcher().m_patch

import pprint
pp=pprint.pprint


def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except TypeError:
            print(f"{func.__name__} only takes numbers as the argument")
    return inner_function