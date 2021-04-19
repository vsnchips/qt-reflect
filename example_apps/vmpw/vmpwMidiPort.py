import rtmidi
from rtmidi import midiutil

import threading
import time

theLock = threading.Lock()
global_running = True


inport = None

from livecoding_helpers import exception_handler

def midi_error(error,foo,bar):
	[print( m) for m in (error,foo,bar)]



from qtpy.QtWidgets import QWidget,QVBoxLayout,QPushButton,QTextEdit,QLabel
from qtpy.QtCore import QTimer

from functools import partial


def default_message_callback(self,message):
	self.messageBox.setText(
					str(message)
					)
	self.update()
	print(message)
	
class vmpwMidiWidget(QWidget):
	def __init__(self,callback=default_message_callback):
		super(vmpwMidiWidget,self).__init__()

		self.setWindowTitle('vmpw Midi Reader')
		self.layout=QVBoxLayout(self)
		self.refreshButton=QPushButton("List Midi In Ports")
		self.refreshButton.clicked.connect(self.listMidiIns)
		self.layout.addWidget(self.refreshButton)
		
		self.readButton=QPushButton("Read Midi Messages")
		self.layout.addWidget(self.readButton)

		self.ins=midiutil.rtmidi.MidiIn(rtmidi.midiutil.get_api_from_environment())
		self.ins.set_error_callback(midi_error)

		self.inport=None
		self.inputButtons=[]
		_i=0
		for port in self.listMidiIns(): 
			button=QPushButton(str(port))
			button.clicked.connect( lambda:self.set_input(1) )
			_i=_i+1
			self.layout.addWidget(button)
			self.inputButtons.append(button)
		self.i=None

		#Monitor
		self.messageBox=QLabel('')
		self.layout.addWidget(self.messageBox)	

		timer=QTimer(self)
		timer.setInterval(1)
		timer.timeout.connect(self.getmessages)
		timerID=timer.start(1000//60)
		self.timer=timer

		self.callback=callback
		self.show()

	#@exception_handler
	def set_input(self,i):
			
			print('Setting {}',format(i))
			if(self.inport is not None): self.ins.close_port()
			self.inport=self.ins.open_port(i)
			global inport
			inport = self.inport
			self.i=i

	def listMidiIns(self):
		ports=self.ins.get_ports()
		for port in ports:
			print(type(port))
			print((port))
		return ports

	def getmessages(self):

		try:
			if(inport is not None):	
				with theLock:
					spin = global_running 
					if (not global_running):
						print("Closing Midi Port")
						inport.close_port()
						return
				message = inport.get_message()
				if (message != None):
					
					self.callback(self,message)
					#self.messageBox.repaint()
					return message
		except Exception as e:
			print(e)
		return None


	def closeEvent(self,event):
		self.ins.close_port()
		if (self.i is not None):	print("Closing port {0}".format(self.i))

