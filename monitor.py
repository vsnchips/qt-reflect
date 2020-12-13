'''
By Daniel Aston, daniel@realithyvirtual.co
v. alpha 1.0.0
This script defines a monitoring framework for any component in an RV grooming or training pipeline.
'''

import zmqSerialSocket
from App.utils.logger import create_logger
from multiprocessing import queues
from qtpy.QtWidgets import QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSplitter, QTextEdit, QWidget
from qtpy.QtWidgets import QWidget, QFrame, QTextEdit
from qtpy.QtCore import Qt, QTimer
from qtpy.QtGui import QImage, QPixmap

import numpy as np

import queue
import threading
import multiprocessing as mp
import zmq

import traceback

zmqArrayContext = zmqSerialSocket.SerializingContext()
    
# Monitor Widget
class rv_MonitorWidget(QWidget):
    ''' An rvMonitorWidget sends stop/start/control messages to its monitorable task. '''

    # This has a spinning update.
    def __init__(self,monitorable,name='Unnamed Monitor Widget',frameRate=60,zmqArrayContext=zmqArrayContext):
        super(rv_MonitorWidget,self).__init__()
        self.name=name
        self.setWindowTitle(name)
        self.monitorable=monitorable

        # Logging Queue Server
         #TODO: Override for the multiprocessing case
        self.zmqContext = zmqArrayContext
        self.logQ = self.zmqContext.socket(zmq.PAIR)
        address=f'inproc://{self.name}_WidgetLogSock'
        print(f"Widget LogView Binding to address: {address}")
        self.logQ.bind(address)

        # Image and Array Monitor Queue
        self.frameGetQ = zmqArrayContext.socket(zmq.PAIR)
        address=f'inproc://{self.name}_FrameSockPair2'
        self.frameGetQ.connect(address)

        #Tick Timer
        self.timer=QTimer();
        self.timer.setInterval(1000//frameRate)  #60 fps
        self.timer.timeout.connect( self.update )
        self.timer.start()

        ############################### Layout ################################
        lay = QHBoxLayout()
        self.setLayout(lay)

        #Main Code / Monitor Splitter
        self.split=QSplitter(Qt.Horizontal)
        self.split.setHandleWidth(12)  
        self.layout().addWidget(self.split)

        # Init / Run Splitter
        self.codeSplitter = QSplitter(Qt.Vertical)
        self.codeSplitter.setHandleWidth(12)
        codeBox=QTextEdit("Runnable code goes here"); codeBox.setFrameShape(QFrame.StyledPanel)
        self.codeSplitter.addWidget(codeBox)
        self.codeBox=codeBox
        self.split.addWidget(self.codeSplitter)
       
        #Monitor/Log Splitter
        self.viewSplit=QSplitter(Qt.Vertical)
        stateView=QLabel()
        stateView.setScaledContents(True) # Override this with more widgets
        self.stateView=stateView
        self.viewSplit.addWidget(stateView)
        
        log = QTextEdit(); log.setFrameShape(QFrame.StyledPanel)
        self.logView = log
        self.viewSplit.addWidget(log)

        self.split.addWidget(self.viewSplit)

        self.setStyleSheet("color: white;"
                        "background-color: #333333;"
                        "selection-color: yellow;"
                        "selection-background-color: brown;"
                        )
        self.show()
         ################################# END LAYOUT #########################
    
    def loggerIn(self,text):
        self.logView.setText(self.logView.text)

    def update(self):
        #Fetch and dispaly results and statistics
        #assets=self.monitorable.log
        #for ass in assets:
        #    try:
        #        self.myWidgets[ass.key]
        #    except KeyError:
        #        self.myWidgets[ass.key] = ass.makeWidget()
        
        
        self.pollLogQueue()
        self.pollFrame()

    def pollFrame(self):
        while self.frameGetQ.poll( timeout = 1)> 0:
            print("Getting Frame")
            imdata=self.frameGetQ.recv_array(copy=False)
            self.imdata=imdata
            self.im=QImage(imdata,imdata.shape[1],imdata.shape[0],QImage.Format_RGB888)
            self.pxm=QPixmap.fromImage(self.im)
            self.stateView.setPixmap(self.pxm)
            
    def pollLogQueue(self):
        while self.logQ.poll( timeout = 1 ) > 0:
            msg=self.logQ.recv_string()
            self.logView.append(msg)
            vs=self.logView.verticalScrollBar()
            vs.setValue(vs.maximum())

# Edits global scope source code in a text box.

# gets tail -n of the log

# Monitorable classes have logs, and monitoring widgets.
# They are useful to monitor persistent objects which perform 
# ongoing tasks.

# Monitorable Object:
class rv_Monitorable:
    ''' A monitorable object is simply a class which has:
     - logging 
     - a watching widget object
     - implementations are responsible for threadsafe methods for the gui to call to get its state.
     '''

    def __init__(self,name="Unnamed Monitorable Object",parent=None,widget=None,frameRate=60,exlocals={}):
        
        ''' Exlocal is for getting the local scope of the constructor caller. (ie an IPython terminal)
        '''
        self.name = name
        self.parent=parent
        
        self.exlocals=exlocals    
    
        #zmqArrayContext = zmqSerialSocket.SerializingContext()
        #TODO: Possible Make this optional.
        
        #self.frameSendQ = zmqArrayContext.socket(zmq.REP)
        #address=f'inproc://{self.name}_FrameSock'
        self.frameSendQ = zmqArrayContext.socket(zmq.PAIR)
        address=f'inproc://{self.name}_FrameSockPair'
        self.frameSendQ.bind(address)

        self.widget = widget
        if widget is None:
            self.widget = rv_MonitorWidget(self,name=name,frameRate=frameRate,zmqArrayContext=zmqArrayContext)
        self.LOGGER = create_logger(self.name,widget=self.widget )
        
    # TODO: Dunno if this is threadsafe
    def float(self):
        self.widget.setParent(None);
        self.widget.show();
    
    def dock(self):
        self.widget.setParent(self.parent);
        self.widget.show();

    #Convenience methods
    def logdebug(self,msg):
        self.LOGGER.debug(msg)
    def logwarning(self,msg):
        self.LOGGER.warning(msg)
    def logerror(self,msg):
        self.LOGGER.error(msg)
    def loginfo(self,msg):
        self.LOGGER.info(msg)
    
# Monitorable Looper Classes:
class rv_MonitorableRepeatable(rv_Monitorable):

    ''' An rv_MonitorableRepeatable is a monitorable object
    with a repeating update to be called from a given thread or process' event loop. 
    
    It has start / stop controls.
    '''

    def __init__(self,name="Unnamed",frameRate=60,**kwargs):

        '''
        rv_MonitorableRepeatable overrides its monitoring widget with code execution buttons etc.
        '''
        super().__init__(name=name,frameRate=frameRate,**kwargs)

        cb = self.widget.codeBox;
        cb.setParent(None)

        icb = QTextEdit('Initialisation code goes here')
        self.widget.initCodeBox=icb
        
        ctlbuts=[]
        ctlButtons=QWidget()
        ctlButtons.setLayout(QHBoxLayout())
        for ctl in ('Init','Run Once','Kill'):
            but=QPushButton(ctl); but.show()
            ctlbuts.append(but)
            ctlButtons.layout().addWidget(but); but.show()
        self.widget.ctlButtons = ctlButtons
        #Hook up ctl connections
        self.widget.ctlButtons.children()[1].pressed.connect(self.initializeFromCode)
        self.widget.ctlButtons.children()[2].pressed.connect(self.runCode)

        #Replace the codeBox with the new assembly
        codeWidget=QSplitter(Qt.Vertical)
        codeWidget.addWidget(icb)
        codeWidget.addWidget(cb)
        codeWidget.addWidget(self.widget.ctlButtons)
        self.widget.codeSplitter=codeWidget

        self.initialize(**kwargs)
    
    def initializeFromCode(self,**kwargs):
        self.run(self.widget.initCodeBox.toPlainText(),exlocals=self.exlocals)

    def runCode(self,**kwargs):
        self.run(self.widget.codeBox.toPlainText(),exlocals=self.exlocals)
        
    def run(self,code,exlocals={}):
        try:
            exlocals=exlocals
            exec(code,globals(),locals())
        except Exception as e:
            self.logerror(traceback.format_exc())
            print(traceback.format_exc())

    def iterate(*iterargs,**kwiterargs):
        if self.enabled:
            dispatch[self.name]['run']()

    def initialize(self,**initArgs):
        self.logwarning("Initialisation not implemented")
    def enable(self):
        self.enabled=True
    def disable(self):
        self.enabled=False

class rv_MonitorableLoop(rv_MonitorableRepeatable):

    ''' Base class for rv_MonitorableThread and rv_MonitorableProcess.
        It adds a message queue system to poll events and runnable execs etc.

        It overrides enable/disable controls to communicate with its looper.
        Adds launch, continue, pause, and terminate buttons.

    '''
    
    def __init__(self,mq=None,**kwargs):
        if mq is None:
            print("mq is None. rv_MonitorableLoops require message queues.")
            raise Exception
        self.mq=mq
        super().__init__(**kwargs)

    def doMessages(self):
        while(self.mq.qsize()>0):
            try:
                self.interpretControl( self.mq.get() )
            except Exception as e:
                self.log("Exception getting message:")
                self.log(traceback.format_exc())

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
        except Exception as e:
                    print(e)
                
    def launch(self,*args,**kwargs):
        self.initialize(*args,**kwargs)
        self.loop()

    def loop(self):
        while(not self.closing):
            self.doMessages()
            if (self.enabled):
                self.iterate()
        
class rv_MonitorableThread(rv_MonitorableLoop):
    ''' An rv_MonitorableThread is an rv_MonitorableLoop running in its own thread '''
    def __init__(self,mq=None,**kwargs):
        self.mq=mq
        if (mq is None):
            self.mq = queue.LifoQueue()
        super().__init__(mq=self.mq,**kwargs)
        self.thread = threading.Thread(target=self.launch, args=())
        self.thread.start()        

class rv_MonitorableProcess(rv_MonitorableLoop):
    ''' An rv_MonitorableThread is an rv_MonitorableLoop running in its own process '''
    def __init__(self,mq=None,**kwargs):
        self.mq=mq
        if (mq is None):
            self.mq = mp.Queue()
        super().__init__(mq=self.mq,**kwargs)
        self.process=mp.Process(target=self.launch,args=launchArgs)
        self.process.start()

#Examples:
class reTestPete(rv_MonitorableRepeatable):
    ''' Testing the repeater class '''
    def __init__(self,runnable=None,**kwargs):
        super().__init__(**kwargs)
        self.runnable=runnable
    def initialize(self):
        self.data="Opening State"
    def go(self,*args,**kwargs):
        if (self.runnable is not None):
            try:
                self.runnable(self,*args,**kwargs)
            except Exception as e:
                self.logerror(traceback.format_exc())

class webcamViewer(rv_MonitorableRepeatable):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.initialize(**kwargs)

    def initialize(self, **initArgs):
        self.vid=cv2.VideoCapture()
        self.vid.open(0)

class rv_inferenceThread(rv_MonitorableThread):
    '''
    rv_inferenceThread does style transfer on the webcam and stores it in a numpy array
    '''
    def __init__(self,name="StyleTransferExampleThread",**kwargs):
        super().__init__(**kwargs)
    def initialize():
        pass
    def iterate():
        pass