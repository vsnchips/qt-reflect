#UberScene Renderer


from glumpy import app, gl, gloo
import numpy as np

import time

fragment=open('uberShader.frag','r').read()

vertex = '''
attribute vec2 a_position;
varying vec2 fragCoord;

void main()
{
    gl_Position = vec4(a_position, 0.0, 1.0);
    fragCoord = a_position;
}
'''

program = gloo.Program(vertex,fragment,count=4)

program['a_position'] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
program['iGlobalTime'] = 0.0


#self.glFunc = '''
#        gl.glClear(gl.GL_COLOR_BUFFER_BIT);
 #       gl.glClearColor(0.5+0.5*sin(time.time()*3),1.0,0.0,1.0)
  #      '''

def draw():
	#Background Scene
	
	#Get uniforms
	arr=np.array( [range(i,i+4) for i in range(8) ] );arr

	#program['iControlChannels[7]']=[1,1,1,1]
	#program['iControlChannels'] = arr
	
	program['a_position'] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
	program['iGlobalTime'] = time.time()%8192

	program.draw(gl.GL_TRIANGLE_STRIP)

