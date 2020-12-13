import OpenGL.GL as gl

import time
from math import *

from PyQt5.QtWidgets import QOpenGLWidget,QMessageBox
from PyQt5.QtCore import QTimer, QObject, QSize, Qt


import traceback as tb

class vmpw_GL(QOpenGLWidget):

    '''Base class for vmpw OpenGL windows
        Connects to 
    '''

    def __init__(self,livebind=None,timer=None):
        super(vmpw_GL,self).__init__()
        
        self.setWindowTitle("VMPW")

        self.errorPopup=QMessageBox()

        self.timer=timer
        if (timer is None): 
            self.timer=QTimer(self)

        self.timer.setInterval(1000//60)
        self.timer.timeout.connect(self.update)
        self.tID = self.timer.start()

        #Hook up live bindings
        self.liveMap=livebind

        self.go()

        self.show()
    
    def go(self):
        self.enabled=True
        self.timer.start()

    def stop(self):
        self.enabled=False
        self.timer.stop()

    import traceback
    def paintGL(self):
        self.time = time.time()
        #print(self.time)

        try:
            #exec(self.glFunc,locals(),globals())
            if (self.enabled): self.liveMap['paintGL']()
            
        except Exception as e:
            self.log("Exception getting message:")
            self.log(traceback.format_exc())


    def error(self,err):
        
        self.stop()   
        self.err=err
        #print(err)
        ep=self.errorPopup
       # ep.close()
        ep.setWindowTitle("OpenGL Window Error")
        ep.setText(str(err) + tb.format_exc())
        ep.setModal(False)
        ep.show()


