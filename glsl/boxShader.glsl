
//Appearance
float fd;
vec3 fog, ac, bc;
vec3 lkey,lamb;


//Getting UV coords
vec2 uvs(vec3 p){
    return p.xy;
}

///////////FOREGROUND////////////////////////////


float sceneFG(vec3 p){
    float d=9999;

    //p = vTunnel(p.zyx);
    d = min(d, 1*texDF(p/(7+1*LFO[0])));

    d-= 0.006*snoise(p/LFO[5]);

//    d = min(d,1*fField0(p));
//    d = min(d,1*fField1(p*1.0));

    return d;
}   

//Finding the normal -
vec3 normalFG(vec3 p){
    #define EPSFG -0.02
    float d = sceneFG(p);
    return normalize( vec3(
    d- sceneFG( vec3( p.x + EPSFG, p.y , p.z )),
    d -sceneFG( vec3( p.x, p.y + EPSFG, p.z )),
    d- sceneFG( vec3( p.x, p.y , p.z + EPSFG))
    ));
}

marchResult marchFG( vec3 o, vec3 r ){ 
    
    r=normalize(r); 
    vec3 p = o;
    vec3 uvw = vec3(0); 
    float d = 9999.0;
    #define MAX_FG_STEPS 256
    
    #define MIND_FG 0.01*(1+LFO[4])    
    for (int i = 0; i < MAX_FG_STEPS; i++){ 
        d=sceneFG(p); 
        p+=d*r; 
        if(d<MIND_FG) break;
    } 
    vec2 uv = uvs(p); 
    return marchResult(p, uv, length(p-o),d, 1); 
}

/////////////BACKGROUND///////////////////////////////////


float sceneBG(vec3 p){      // Scene Description Here 
    float d;
    
    //Domain warping
    p.xy = euc2pol(p.xy);

    //Scene Selection  
     d=boxWorld(p);
    return d;
}

marchResult marchBG( vec3 o, vec3 r ){ 
    
    r=normalize(r); 
    vec3 p = o;
    vec3 uvw = vec3(0); 
    float d = 9999.0; 
    #define MAX_STEPS 256 
    #define MIND_BG 0.001//0.01*(1+LFO[4])  
    
    for (int i = 0; i < MAX_STEPS; i++){ 
        d=sceneBG(p); 
        p+=d*r; 
        if(d<MIND_BG) break;
    } 
    vec2 uv = uvs(p); 
    return marchResult(p, uv, length(p-o), d, 1); 
}

/////////////////////////////////////////

//Finding the normal -
vec3 normalBG(vec3 p){
    #define EPS -0.1
    float d = sceneBG(p);
    return normalize( vec3(
    d- sceneBG( vec3( p.x + EPS, p.y , p.z )),
    d- sceneBG( vec3( p.x, p.y + EPS, p.z )),
    d- sceneBG( vec3( p.x, p.y , p.z + EPS))
    ));
}

//RENDER MAIN
void main(  )
{
    // Time varying pixel color 
    vec2 _uv = fragCoord.xy/iResolution.xy;
    _uv=vUV.st;

    setWorldGlobals();

    //Ray init
    vec2 uv=_uv.xy*2.-vec2(1.);
    uv.x *= iResolution.x/iResolution.y;
    vec4 ray=vec4(uv,1.0,1.);
   
    //World Transform
    
    //translate
    vec4 wbg = vec4(0,0,-10,1);
    
    //rotate
    mat4 vr;
    
    //Background
    vr= rollMat(0.)*pitchMat(0.6)*yawMat(TT[1]);
    vec4 raybg = ray * vr; wbg*=vr;  
    //marchResult bg = marchBG( wbg.xyz, raybg.xyz );         
    marchResult bg = marchThis(wbg,raybg,0);
   
    //Foreground    
    vr= rollMat(0.)*pitchMat(0.)*yawMat(0.5*LFO[3]);
    vec4 wfg = vec4(0,0,-2,1);
    vec4 rayfg = ray * vr; wfg*=vr;           
    marchResult fg = marchFG( wfg.xyz, rayfg.xyz );
   
    // Normalized pixel coordinates (from 0 to 1) 
    vec3 norm = //bg.t < fg.t ?
     normalBG(bg.p)  ;
     // : -normalFG(fg.p);
    vec3 col = vec3(0.); 

    col += 0.5*norm+0.5;
    col= norm;
    
    //Fog
    col /=  max(1, 0.2*
    (min(fg.t,bg.t)));

    col = clamp(col,0,1);
    //col=tint( col, 0.5+0.5*LFO[2], 10);
    col=tint( col, 0.6, 4);

    /*col -=0.1; */
    col += 0.4*hsv2rgb(vec3(0.8,0.2,1));
    
    col.rgb = col.grr;

    // Output to screen
    fragColor = vec4(col,1.0);
}
