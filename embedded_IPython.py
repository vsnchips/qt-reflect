# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 16:15:56 2020
@author: Dan Aston
"""

import os,sys

sys.path.append(os.path.realpath('.'))

# Import the console machinery from ipython
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.inprocess import QtInProcessKernelManager
from IPython.lib import guisupport

os.environ['QT_API'] = 'PyQt5'
from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5.QtWebEngine import *
from PyQt5.QtWebEngineCore import *
from PyQt5.QtWebEngineWidgets import *

from livecoding_helpers import *
from devBox import * 

import pkg_resources

class QIPythonWidget(RichJupyterWidget):
    """ Convenience class for a live IPython console widget. We can replace the standard banner using the customBanner argument"""
    def __init__(self,customBanner=None,*args,**kwargs):
        if not customBanner is None: self.banner=customBanner
        super(QIPythonWidget, self).__init__(*args,**kwargs)
        self.kernel_manager = kernel_manager = QtInProcessKernelManager()
        kernel_manager.start_kernel()
        kernel_manager.kernel.gui = 'qt4'
        self.kernel_client = kernel_client = self._kernel_manager.client()
        kernel_client.start_channels()

        self.syntax_style="monokai"


        def stop():
            kernel_client.stop_channels()
            kernel_manager.shutdown_kernel()
            guisupport.get_app_qt4().exit()            
        self.exit_requested.connect(stop)

    def pushVariables(self,variableDict):
        """ Given a dictionary containing name / value pairs, push those variables to the IPython console widget """
        self.kernel_manager.kernel.shell.push(variableDict)
    def clearTerminal(self):
        """ Clears the terminal """
        self._control.clear()    
    def printText(self,text):
        """ Prints some plain text to the console """
        self._append_plain_text(text)        
    def executeCommand(self,command):
        """ Execute a command in the frame of the console widget """
        self._execute(command,False)

rootCons=None
rootWidget=None

gTEst = None

class LiveConsole(QWidget):
    def __init__(self, parent=None,workFile=None,liveApp=None):

        ''' The LiveConsole is an ipython interpreter window which shares the global namespace with this module. '''
        super(LiveConsole,self).__init__(parent=parent)

        #lLayout
        layout = QVBoxLayout(self)
        self.ipyConsole = QIPythonWidget(customBanner="Welcome to the embedded ipython console\n")
        layout.addWidget(self.ipyConsole)        
        self.ipyConsole.printText("Hello Qt Embedded IPython")                           

        #Styling
        self.setWindowTitle('Live Console')

        global rootCons,rootWidget
        rootCons = self.ipyConsole
        rootWidget = self
        rootWidget.setStyleSheet("color: white;"
                "background-color: #333333;"
                "selection-color: yellow;"
                "selection-background-color: brown;"
                "background:translucent"
                )
        rootCons.setStyleSheet("color: white;"
                "background-color: dark-grey;"
                "selection-color: yellow;"
                "selection-background-color: brown;"
                "background:translucent"
                )


    # Loading the work script
        workScript=None
        if (workFile): workScript=open(workFile,'r').read()

        # Scope Sharing
        app = liveApp
        __name__ = "__interpreter__"
        rootCons.pushVariables(dict(globals(),**locals()))    

        if (workScript):rootCons.execute(workScript)

        initScript='''#Monokai script
for widget in self.children(): 
    try:
        widget.setStyleSheet(pkg_resources.resource_filename("jupyter_qtconsole_colorschemes","{}.css".format("monokai"))) 
    except Exception as e:
            tb.print_exc()
            pass'''
        rootCons.execute(initScript)

def print_process_id():
    print ('Process ID is:', os.getpid() )       

widget=None
liveApp=None

def main():

    global globalTest, liveApp

    globalTest=20
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])

    startScript = None
    if (len(sys.argv) > 1 ):
        startScript = sys.argv[1] 
    widget = LiveConsole(workFile=startScript,liveApp=app)
    widget.setStyleSheet("background:translucent")

    widget.show()

    globalTest=10

    app.exec_()    

if __name__ == '__main__':
    main()
