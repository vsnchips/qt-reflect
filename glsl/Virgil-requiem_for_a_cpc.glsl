
//***************************************************************************************************
//
// Requiem for a CPC  /  Haujobb and Alcatraz
// Jochen "Virgill" Feldkoetter
//
// 4k Intro for Nordlicht demoparty 2016      Shadertoy version
//
//***************************************************************************************************


//***************************************************************************************************
// particle function
//***************************************************************************************************

float particles(vec3 direction)
{
	float accumulate=0.;
    const mat3 p=mat3(13.3,23.5,21.7,21.1,28.7,11.9,21.8,14.7,61.3);
	vec2 uvx=vec2(direction.x,direction.z)+vec2(1.,iResolution.y/iResolution.x)*gl_FragCoord.xy/iResolution.xy;
	float DEPTH = direction.y*direction.y-.3;
	for (float fi=0.;fi<10.;fi++) 
	{
		vec2 q=uvx*(1.+fi*DEPTH)+vec2(DEPTH,0.2*iTime/(1.+fi*DEPTH*.03));
		vec3 n=vec3(floor(q),31.1+fi);
		vec3 m=floor(n)*.0001 + fract(n);
		vec3 r=fract((31415.+m)/fract(p*m));
		vec2 s=abs(mod(q,1.)-.5+.9*r.xy-.45);
		float d=s.x+s.y+0.7*max(s.y,s.x)-.01;
		float edge=.06;
		accumulate+=smoothstep(edge,-edge,d)*r.x;
	}
	return accumulate;
	}

//***************************************************************************************************
// map
//***************************************************************************************************


float scene(vec3 p)
{
//	super waves
    if (efx_==0) return fField0(p/6.0);
//	pyramid carpet
    if (efx_==1) return fField1(p/6.0);	
//	wormhole tunnel  
    if (efx_==2) p=p.xzy;  
//  fancy tunnel
    if (efx_==3){
		p= vTunnel(p.xzy);
	}

    p.xy = vec2( (atan(p.x,p.y)+1.5*sin(0.9*sqrt(dot(p.xy,p.xy))-0.5*TT[0]))*1.0187,1.-length(p.xy));
	return fField1(p);
    
}


//***************************************************************************************************
// softshadow
//***************************************************************************************************

float shadowsoft( vec3 ro, vec3 rd, float k )
{
	float t=.1;
	float res=1.;
    for (int i=0;i<25;++i)
    {
        float h=scene(ro+rd*t);
        if (h<0.001) return 0.;
		res=min(res,k*h/t);
        t+=h;
		if (t>0.23) break;
    }
    return res;
}

//***************************************************************************************************
// normal calculation
//***************************************************************************************************

vec3 calcNormal(vec3 pos)
{
    float eps=0.04; pos-=0.01;
	float d=scene(pos);
	return normalize(vec3(scene(pos+vec3(eps,0,0))-d,scene(pos+vec3(0,eps,0))-d,scene(pos+vec3(0,0,eps))-d));
}

//***************************************************************************************************
// marching outside sdf
//***************************************************************************************************

float castRay(vec3 ro,vec3 rd) 
{
    float precis=.0001;
    float h=precis*2.;
    float t=0.;
	for(int i=0;i<100;i++) //*************************************
	{
        if(abs(h)<precis||t>12.) break;
		h=scene(ro+rd*t);
        t+=h;
	}
    return t;
}

//***************************************************************************************************
// marching inside sdf
//***************************************************************************************************

float castRay2(vec3 ro,vec3 rd) 
{
//	tunnel effects
    float precis=.01;
//	super waves
    if (efx_==0) precis=.3;
//	mirror carpet
    if (efx_==1) precis=.8;
    float h=0.;
    float t=.1;
    for(int i=0;i<40;i++) 
	{
		if(abs(h)>precis) break;
		h=scene(ro+rd*t);
		t-=h;
	}
	return t;
}


//***************************************************************************************************
// main
//***************************************************************************************************

void main()
{

// time control (only in shadertoy)

    if (iTime<136.) efx_=2;
    if (iTime<102.) efx_=0;
    if (iTime<68. ) efx_=1;
    if (iTime<34. ) efx_=3;
    
    
    vec2 uv,p;
	uv=gl_FragCoord.xy/iResolution.xy; 
    p=uv*2.-1.;
   	p.x*=iResolution.x/iResolution.y;
	
//  camera
    float theta=sin(iTime*.1)*6.28;
    float x=3.*cos(theta); 
    float z=3.*sin(theta);
	vec3 ro=vec3(x*2.2,5.+2.*sin((iTime+37.)*.15), z*1.4);		
	if (efx_==2||efx_==3) ro=vec3(0.,8.,.01);
    if (efx_==0) ro.y+=1.6; //*******************************************
	vec3 cw=normalize(vec3(0.,.25,0.)-ro);
    vec3 cu=normalize(cross(cw,vec3(0.,1.,0.)));
	vec3 rd=normalize(p.x*cu+ p.y*(cross(cu,cw))+7.5*cw);

// 	render:
	float t=castRay(ro,rd);
	vec3 pos=ro+rd*t;
	vec3 nor=calcNormal(pos);

// 	lightning:
	vec3 ligvec=vec3(-.5,.2,.5);
	if (efx_==2) ligvec=vec3(-.3*cos(iTime),-.2,.5*sin(iTime*1.9)+.2);
    
	vec3 lig=normalize(ligvec);	
    float dif=max(dot(lig,nor),0.);
    float spec=pow(max(dot(reflect(rd,nor),lig),0.),32.);
	vec3 col=vec3(.1*dif+1.*spec);
    if (efx_==1) col+=.5*ku.x;
    
//	new shadow
	float sh=shadowsoft(pos,lig,1.2); 
    col*=clamp(sh,.4,1.);

    
//	refraction 1st pass
	vec3 te,dif2,rd2,pos2,nor2,ro3,rd3,pos3,nor3;
	rd2=refract(rd,nor,.78);  
    te.x=castRay2(pos,rd2);
	pos2=pos+rd2*te.x;
    nor2=calcNormal(pos2);
	dif2.x=clamp(dot(lig,nor2),0.,1.);
    
	rd2=refract(rd,nor,.82);
    te.z=castRay2(pos,rd2);
	pos2=pos+rd2*te.z;
    nor2=calcNormal(pos2);
	dif2.z=clamp(dot(lig,nor2),0.,1.);
    
	rd2=refract(rd,nor,.8);
    te.y=castRay2(pos,rd2);
	pos2=pos+rd2*te.y;
    nor2=calcNormal(pos2);
	dif2.y=clamp(dot(lig,nor2),0.,1.);
    
    float spec2=pow(clamp(dot(reflect(rd2,nor2),lig),0.,1.),32.);
    col+=.3*spec2;
    
    te=clamp(te,0.,1.);
    col+=(1.-te*.25)+(1.-t*.15)*dif2;
    
//	double shadow on tunnel effects
    if (efx_==2||efx_==3) col*=clamp(sh,.4,1.);    
    
// 	refraction 2nd pass
	ro3=pos2+rd; 
	rd3=rd2+0.05;
    float t3=castRay(ro3,rd3);
	pos3=ro3+rd3*t3;
    nor3=calcNormal(pos3);
	float dif3=clamp(dot(lig,-nor3),0.,1.);
    col-=.2*(1.-dif3);

//  add more color depth
	col=mix(col,vec3(.5,.4,.4),ku.y*.2*te.z);

//	tunnel depth and particles    
    float particlevar=.35*(particles(cw)-particles(vec3(cw.x,cw.y,cw.z+rd.z)));
    vec3 deep=vec3(1.);
    if (efx_==2||efx_==3) 
    {
        deep=clamp(1.-vec3(t*t)*.007,0.,1.);
    	particlevar=0.;
    }

// 	postprocessing
	col-=.3*noise(.4*rd3*iTime);									
	col*=.9+.1*sin(uv.y*800.);	
    col-=1.-dot(uv,1.-uv)*2.5;
    fragColor=vec4((deep*col+particlevar),0.);
}



