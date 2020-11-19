#%%
import sys
preIncluded='PySide2' in sys.modules
sys.path.append('.')
from livecoding_helpers import *
import PyQt5
import os,sys
from PyQt5.QtGui import QPixmap, QResizeEvent
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QLabel, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import QTimer, QObject, QSize, Qt

#Custom PyQt Modules
from pyqtconsole.console import PythonConsole

from PIL import Image

import glob
import multiprocessing as mp
import queue
EmptyException=queue.Empty

#if(not preIncluded): app=QApplication(sys.argv)

# %%
# This is like Watch, or Tail, for images.

class LiveMonitor(QWidget):

    """ The base QWidget class for RV guis, with a simple frame tick and communication functionality added. """

    def __init__(self,interface=None,title="VMPW Live Dev"):
        super(LiveMonitor,self).__init__()

        #Hook up messaging and control
        if (interface is not None):
            self.inbox=interface.inbox
            self.logpost=interface.logpost
        else:
            self.inbox=None
            self.logpost=None
 
        #Default Appearance
        self.padding = 5
        self.title = title
        self.setWindowTitle(self.title)
        
        self.vbox=QVBoxLayout()
        self.pixmaps=[]

    def log(self,message):
        if (self.logpost is not None):
            self.logpost.put(message)
    
    def interpretControl(self,message):
        self.log(f"Recieved {message}")
        try:
            if (message['command'] == 'watchsequence'):
                self.watchdir = message['value']
            if (message['command'] == 'exec'):
                try:
                    exec(message['value'],globals(),None)
                except Exception as e:
                    print(e)
            if (message['command'] == 'execfile'):
                try:
                    script = open(message['value'],'r').read()
                    exec(script,globals(),None)
                    #execfile(message['value'],globals())
                except Exception as e:
                    print(e)
        
        except KeyError:
            self.log("Recieved control message with no command:")
            self.log(message)
        #TODO more commands go here. At the moment we want to look at new sequences.

   
    def domessages(self):
        if(self.inbox is not None):
            try:
                self.interpretControl(self.inbox.get(timeout=0.010))
            except EmptyException as e:
                pass

    def tick(self):
        #Poll control messages
        self.domessages()

        #Update self
        self.update()
        #self.handleScale()
        #self.updatedisplay(self.getNextSet())
        #Post control messages

    '''def update(self):
        pass
    '''
    
    def handleScaleCallBack(self):
        #TODO Delegate this math to a resize event handler
        pass
        
def makeLive(interface):
    app=QApplication(sys.argv)
    mon=LiveMonitor(interface=interface)

    #Setup tick
    timer = QTimer(mon)
    timer.setInterval(1)
    timer.timeout.connect(mon.tick)
    timerID=timer.start(1000//60)

    mon.show()
    sys.exit(app.exec_())

def launchLive():
    logQ=mp.Queue()
    inQ=mp.Queue()
    interface=rvGuiInterface(logQ,inQ)

    #global makeLive
    
    guiprocess=mp.Process(target=makeLive,args=(interface,))
    guiprocess.start()

    return interface

class rvGuiInterface():

    """ This is the object which the main process has an instance of, and uses to communicate with the gui process """

    def __init__(self,inbox,logpost):
        self.inbox=inbox
        self.logpost = logpost

    def printlog(self,tout=0.05):
        try:
            while True:
               print(self.logpost.get(timeout=tout))
        except EmptyException as e:
            pass

    def exec(self,code):
        self.inbox.put({'command':'exec','value':code})
        self.printlog()

    def execfile(self,code):
        self.inbox.put({'command':'execfile','value':code})
        self.printlog()

def gxf(code):
    gui.exec('execfile(' + code + ', globals() )')
if __name__=='__main__':
    pass

    #import time; time.sleep(5)
    #gui=launchLive()
    #gui.execfile(sys.argv[1])

    #gx=gui.exec
    #gxf=gui.execfile