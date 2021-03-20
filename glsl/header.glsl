precision mediump float;

uniform float[256] iFFT;
uniform float[256] iAudioBuffer;
uniform float[32] iControlChannels;

uniform vec4 iResolution;
uniform float iTime;

out vec4 fragColor;

//TouchDesigner Adaptions
#define fragCoord vUV

//Scene Globals
//anim
float time, bs, ss;
//Control voltages/ lfos
float LFO[6];
float TT[6];

vec3 COLOR[6];

struct marchResult{
    vec3 p;
    vec2 uv;
    float t;
    float d;
    int objID;
}mr;