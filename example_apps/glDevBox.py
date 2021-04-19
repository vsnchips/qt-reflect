from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from pyqode.core.widgets import TextCodeEdit

from devBox import *

from vmpwGLViewport import *
class glDevBox(QWidget):
      
    def __init__(self):
        super().__init__()	
        self.initUI()	
	
    def initUI(self):
        hbox = QHBoxLayout(self)
        splitter1 = QSplitter(Qt.Horizontal)
                
        editor=liveEditor()
        editor.setFrameShape(QFrame.StyledPanel)
        editor.show()  	
        self.editor=editor
        
        glv = vmpwGLFrameViewer()
        glv.show()
        self.glv=glv

        splitter1.addWidget(editor)
        splitter1.addWidget(glv)
        splitter1.setSizes([100,200])

        hbox.addWidget(splitter1)
        self.setLayout(hbox)
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
                
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('devBox')
        self.show()
    
db1 = devBox()