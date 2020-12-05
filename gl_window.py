import OpenGL.GL as gl

import time

from math import *

from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import QTimer, QObject, QSize, Qt

#Note this is a pure function
def devCallback(self):
     pass
 
class vmpw_GL(QOpenGLWidget):

    '''Base class for vmpw OpenGL windows'''

    def __init__(self,timer=None):
        super(vmpw_GL,self).__init__()
        self.setWindowTitle("VMPW")

        self.glFunc = '''gl.glClear(gl.GL_COLOR_BUFFER_BIT);
gl.glClearColor(0.5+0.5*sin(time.time()*3),1.0,0.0,1.0)
        '''

        self.timer=timer
        if (timer is None): 
            self.timer=QTimer(self)

        self.timer.setInterval(1)
        self.timer.timeout.connect(self.paintGL)
        self.tID = self.timer.start(1000//60)

        self.show()
 
        
    def paintGL(self):
        self.time = time.time()
        #print(self.time)
        try:
            #exec(self.glFunc,locals(),globals())
            devCallback(self)
            
        except Exception as e:
            print(e)
        self.update()

    
    def setGL(self,f):
        self.paintGL = f


