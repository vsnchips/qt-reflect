import gl_window as glw
from livecoding_helpers import *

foo='bar'
whats='it'

#VMPW Modules
from glumpy import gl,gloo
from vmpwMidiPort import * 

app=None
if __name__=='__main__':
	import sys
	from qtpy.QtWidgets import QApplication
	app=QApplication(sys.argv)	


#Uber Scene
import uberScene as us;il.reload(us)
usDev={'paintGL':us.draw}
import gl_window as glw;il.reload(glw)
gl1=glw.vmpw_GL(None)
gl1.liveMap=usDev
gl1.go()

#uniform setting
def setControlChannel(i,val):
    global us
    gl.glUniform1fv(gl.glGetUniformLocation(
        us.program.handle,'iControlChannels')+i,1,val
        )

#Midi
import vmpwMidiPort as midi;il.reload(midi)
import numpy as np
msg=None
chans=np.zeros((4,2,4))
chan=0
chx=None
val=None
def midiCallBack(self,message):
    '''This callback maps the Novation Launch Control XL's knobs and sliders into a (4,2,4) array. Organised in 4 banks. Knobs are indexed top to bottom, sliders are the 4th element. (topknob,middleknob,bottomknob,slider)'''

    global chx,val,chans
    msg=message
    print(message)
    ch=message[0][1]
    #print(ch)
    row = -1   
    if( ch>= 13 and ch<=20):
        chan=ch-13
        row=0 
    if( ch>= 29 and ch<=36):
        chan=ch-29
        row=1
    if( ch>= 49 and ch<=56):
        chan=ch-49
        row=2
    if( ch>= 77 and ch<=84):
        chan=ch-77
        row=3
        
    chx=(chan//2,chan%2,row)
    print(chx)
    val=message[0][2]
    chans[chx]=val
    floatchan = 8*chx[0]+4*chx[1]+chx[2]
    gl.glUseProgram(us.program.handle)
    gl.glUniform1fv(gl.glGetUniformLocation(
        us.program.handle,'iControlChannels')+floatchan,1,val
        )
    
mwidge=midi.vmpwMidiWidget(callback=midiCallBack)

## Set up OSC Server

## Set up aubio input


if __name__=='__main__':
	app.exec_()
