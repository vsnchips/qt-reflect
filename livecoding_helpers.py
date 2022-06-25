print ("Hello Dan's livecoding helpers")
import os
import sys
sys.path.append('.')

import numpy as np
import importlib as il

import pprint
pp=pprint.pprint
import traceback

import pythonosc as pyosc

def preview(image):
    previewName(image,'Preview')

from PIL import Image
def drawImg(img,mode='RGB'):
    return Image.fromarray(img).convert(mode)

def cvshow(name,image):
    import cv2
    cv2.namedWindow(name)
    cv2.imshow(name,image)
    cv2.waitKey(100)

def execfile(file,globs):
    global __name__
    __name__='__mp_main__'
    script= open(file,'r').read()
    exec(script,globs,locals())

class mPatcher:
    @classmethod
    def m_patch(self,state,newdef):
        for k in newdef.__dict__:
            obj=getattr(newdef,k)
            if not k.startswith('_') and callable(obj):
                setattr(state, k, obj)
patch=mPatcher().m_patch

def addToGlobs(module):
    for key in dir(module):
        globals()[key]=getattr(module,key)    

def r2g(module):
    import importlib as il
    il.reload(module)
    addToGlobs(module)
