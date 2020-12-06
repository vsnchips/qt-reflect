#version 320
precision mediump float;

varying vec2 fragCoord;
uniform float iGlobalTime;
uniform vec2 iMouse;

uniform vec4 iControlChannels[4][2];
uniform vec4 iControlButtons[4];

#define STEP_COUNT 10

//just basic clouds from perlin noise
float rand(vec2 co){return fract(sin(dot(co,vec2(12.9898,78.233)))*43758.5453);}
float noyz(vec2 co){
    vec2 d=smoothstep(0.0,1.0,fract(co));
    co=floor(co);
    const vec2 v=vec2(1.0,0.0);
    return mix(mix(rand(co),rand(co+v.xy),d.x),
        mix(rand(co+v.yx),rand(co+v.xx),d.x),d.y);
}
float clouds( in vec2 q, in float tm )
{
    float f=0.0,a=0.6;
    for(int i=0;i<5;i++){
            f+= a*noyz( q+tm );
        q = q*2.03;
        a = a*0.5;
    }
    return f;
}

float getPattern(vec2 uv) {
    //this can be any pattern but moving patterns work best
    float w=clouds(uv*5.0, iGlobalTime*0.5);
    return w;
}

void main(){

    //background pattern:
    vec2 uv = fragCoord;
    
    vec3 c = vec3(getPattern(uv*3));
    float d=1;//=DE(uv);//get distance to objects
    c=mix(vec3(1.0-10.0*d*d),c,smoothstep(0.2,0.25,d));//mix in objects


    //BG post level
    c*=0.2;

    //Debug Uniforms
    ivec2 ctlIndex = ivec2(uv.x*8,uv.y*4);
    int id=4*ctlIndex.x+ctlIndex.y;
    
    vec3 debugctl=vec3(0);

    //debugctl = vec3(vec2(ctlIndex)/32.0,id/32.0);
    
    debugctl.g += iControlChannels[5][0]/32;
    
    c=debugctl;

    //c.b += iControlChannels[2].a;


    gl_FragColor = vec4(c,1.0);
}