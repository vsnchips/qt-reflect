vec2 euc2pol(vec2 uv) {
    return vec2(  atan(uv.x/uv.y ), length(uv));}
    
    //Rotation Mats
    mat4 rollMat(float r){
        return mat4(
        cos(r),-sin(r),0,0,
        sin(r),cos(r),0,0,
        0,0,1,0,
        0,0,0,1
        );
    }
    
    mat4 pitchMat(float r){
        return mat4(
        1,0,0,0,
        0,cos(r),-sin(r),0,
        0,sin(r),cos(r),0,
        0,0,0,1
        );
    }
    
    mat4 yawMat(float r){
        return mat4(
        cos(r),0,sin(r),0,
        0,1,0,0,
        -sin(r),0,cos(r),0,
        0,0,0,1
        );
    }


//COLOR AND POST

// All components are in the range [0…1], including hue.
vec3 rgb2hsv(vec3 c)
{
    vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
    vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
    vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));

    float d = q.x - min(q.w, q.y);
    float e = 1.0e-10;
    return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
}
// All components are in the range [0…1], including hue.
vec3 hsv2rgb(vec3 c)
{
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

vec3 tint_fromTo(vec3 rgb,float h,float from, float to,float k){
    vec3 hsv=rgb2hsv(rgb);
    //hsv.g /= (1+ pow( abs( hsv.r - h), 1/k) );
    float desat = k*abs( hsv.r - h);
    float _t = (1/desat);
    float t = from*(1-_t) + to*(_t);  
    hsv.g *= t;
    
    return hsv2rgb(hsv);
}

vec3 tint(vec3 rgb,float h,float k){
    return tint_fromTo(rgb,h,0,1,k);
}
//

//////////////////////////////////
//just basic clouds from perlin noise

float smin(float a, float b,float k){
    //float diff=pow((a-b),2);
    float diff=abs((a-b));  
    return min(a,b) + (1-log(diff)); 

float rand(vec2 co){return fract(sin(dot(co,vec2(12.9898,78.233)))
*43758.5453);}

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
    float w=clouds(uv*5.0, TT[0]*0.5);
    return w;
}

//////////////////////////// DF's //////////////////////////////////


////////////////////////////////////////////////////////////////////

/////// DF's etc borrowed from Virgil //////
//*********************************************************

//const int efx_ = 3;
int efx_=0;
vec2 ku=vec2(0);

/////////////////////////// TUNNEL DOMAIN ///////////////////////

vec3 vTunnel(vec3 p){
		p.z-=TT[2];
        p/=10;
		return  (sin(p*1.9+TT[0])+sin(p.yzx+TT[0]*2.2))*5.11;
}

//***************************************************************************************************
// noise functions
//***************************************************************************************************

float snoise(vec3 p){
    
    const vec3 s=vec3(7,157,113);	
    vec3 ip=floor(p);    
    vec4 h=vec4(0.,s.yz,s.y+s.z)+dot(ip,s);    
    p-=ip;
    p=p*p*(3.-2.*p);
    h=mix(fract(sin(h)*43758.5453),fract(sin(h+s.x)*43758.5453),p.x);
    h.xy=mix(h.xz,h.yw,p.y);
    return mix(h.x,h.y,p.z);
}

float noise(vec3 n)
{
 	return snoise(n)*.6+snoise(n*2.)*.4;
}

// domain repetition and rotation functions
//*********************************************************
vec2 pMod(inout vec2 p,vec2 size) 
{
    vec2 hz=size/2.;
	vec2 c=floor((p+hz)/size);
	p=mod(p+hz,size)-hz;
	p*=mod(c,vec2(2))*2.-vec2(1);
    if (efx_!=0)
    {
		p-=hz;
		if (p.x>p.y) p.xy=p.yx;
    }
	return floor(c/2.);
}

void pR(inout vec2 p,float a) 
{
	p=cos(a)*p+sin(a)*vec2(p.y,-p.x);
}

//*********************************************************
// sdf box
//*********************************************************
float fBox(vec3 p, vec3 b) 
{
	vec3 d=abs(p)-b;
    return min(max(d.x,max(d.y,d.z)),0.)+length(max(d,0.));
}

//3D DF's:    xyz is uvw, z is distance
float box(vec3 p,float x, float y, float z){ 
        return max(max(abs(p.x)-x,abs(p.y)-y),abs(p.z)-z);
    }


// 	super waves
float fField0(vec3 p)
{
    float fbm_=noise(p*7.);
	pMod(p.xz,vec2(1.8-0.4*fbm_));
	pR(p.xz,iTime*0.2+0.2*fbm_);
	pR(p.xy,iTime*0.4+0.2*fbm_);
	return fBox(p-vec3(0.0),vec3(1.1))-0.15-0.05*fbm_;
}

// 	pyramid carpet & tunnel effects
float fField1(vec3 p) 
{
	ku = pMod(p.xz,vec2(.8));
	pR(p.xz,LFO[0]*.16);
	pMod(p.xz,vec2(.7));
	if (efx_!=3) pR(p.xy,LFO[0]*.334);
	float box=fBox(p-vec3(0),vec3(.6));
    if (efx_==2) box=.05-box;
    if (efx_==1) box-=.02*noise(vec3(0.,0.,p.z)*8.0);
    return box;
}

void setWorldGlobals(){
     time = iTime;
     bs=.5+0.3*sin(time);
     ss=.5+0.3*cos(time);
     
     LFO[0]=sin(time/8.);
     LFO[1]=cos(time/4.);
     LFO[2]=sin(time/2.);
     LFO[3]=cos(time);
     LFO[4]=sin(time*2.);
     LFO[5]=cos(time*6.);
     
     TT[0]=iControlChannels[8]*time/8.;
     TT[1]=time/4.;
     TT[2]=time/2.;
     TT[3]=time;
     TT[4]=time*2.;
     TT[5]=time*6.;

    for (int i=0; i<4; i+=2){
        COLOR[i]= hsv2rgb(
            vec3(iControlChannels[i*2]/127
                ,iControlChannels[i*2+8]/127
                ,iControlChannels[i*2+16]/127
                )
        );

    }
            dfgfd
     COLOR[0]=hsv2rgb(vec3(iControlChannels))
}


//Getting UV coords
vec2 xy_uvs(vec3 p){
    return p.xy;
}
/////////////
    #define MAX_STEPS 256 
    #define MIND_BG 0.001//0.01*(1+LFO[4])  

#define rot(A) {mat2(cos(A),-sin(A),sin(A),cos(A))}