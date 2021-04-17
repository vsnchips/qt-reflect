# VMPW OpenGL Viewport Widget

import numpy as np

#Dummy OpenGL Widget
from PyQt5.QtOpenGL import *
dgl = QGLWidget()
dgl.show()
dgl.initializeGL()
#dgl.show()
from vsnchips_gl.vsnchips_shader import *
from vsnchips_gl.vsnchips_texture import *
from vsnchips_gl.vsnchips_screenquad import *
#dgl.hide()

def paintGL(state):
    import OpenGL.GL as gl
    gl.glClearColor(1,0,1,1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

class vmpwGLFrameViewer(QGLWidget):
    def __init__(self,paint=paintGL,**kwargs):
        super(vmpwGLFrameViewer,self).__init__(**kwargs)
        self.paint=paint      

    def paintGL(self):        
        if(self.paint is not None):
            self.paint(self)

    def update(self):
        pass

preview = vmpwGLFrameViewer(shareWidget=dgl)
preview.show()

#refdefs
def paint_(state):
    global tex
    global texprog
    global buff
        
    import numpy as np
    tex = vsn_Texture(np.asarray(np.random.random((512,512,4)),dtype='float32'))
    vsn_BindTextureToUnit(tex.texture,gl.GL_TEXTURE0)
    buff=gl.glGetTexImage(gl.GL_TEXTURE_2D,0,gl.GL_RGBA,gl.GL_UNSIGNED_BYTE)
        
    s = state.size()
    gl.glViewport(0,0,s.width(),s.height())
    
    gl.glClearColor(0.5,0,1,1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    
    gl.glUseProgram(texprog)
    vsn_BindTextureToUnit(tex.texture,gl.GL_TEXTURE0)
    gl.glUniform1i(gl.glGetUniformLocation(texprog,'aTex'),0)
    buff=gl.glGetTexImage(gl.GL_TEXTURE_2D,0,gl.GL_RGBA,gl.GL_UNSIGNED_BYTE)
   
    screenQuad(texprog)
    buff=gl.glGetTexImage(gl.GL_TEXTURE_2D,0,gl.GL_RGBA,gl.GL_UNSIGNED_BYTE)
    
preview.paint=paint_;preview.repaint()