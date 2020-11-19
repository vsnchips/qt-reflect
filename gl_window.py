import OpenGL.GL as gl

from PyQt5.QtWidgets import QOpenGLWidget

class vmpw_GL(QOpenGLWidget):

    '''Base class for vmpw OpenGL windows'''

    def __init__(self):
        super(vmpw_GL,self).__init__()
        self.setWindowTitle("VMPW")
        pass

    def paintGL(self):
        gl.glClearColor(0.8,0.21,0.5,1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    
    def setGL(self,f):
        self.paintGL = f

