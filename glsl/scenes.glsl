
//Countdown Text
float texDF( vec3 p){
    float thick = .03;
    float d = max( abs( p.z ) - thick ,
        1.0-1.0*texture2D(sTD2DInputs[0],
        p.xy + 0.5
        ).r );
    return 0.125*d;
}

float boxWorld(vec3 p){      // Scene Description Here 
    float d;
    

    // Little boxes
    float es= 2.5 +.15*LFO[4];
    vec3 tp = fract(p)*es - es/2.;
    d = box(tp,bs,bs,bs);
    d = min(d, length(tp) - ss);
    d /= es ;
    
    p = vTunnel(p.xyz);
    
    //Big box 
    d = max(d, box(p, 3.,3.,3.) );
    
    vec3 fp=p + vec3(-2,-10,10);
   //d= min(d, fField0(fp.zxy/5.0));
   
    d =  min(d, fField1( 1.58*vTunnel(fp.xzy)));   
    return d;
}

float mapScene(vec3 p, int content){
    switch( content ){
        case 0:{
            return texDF(p);
        }
        case 1:{
            return boxWorld(p);
        }

    }
    return 9999;

}

marchResult marchScene(vec3 o, vec3 r, int sceneID, int maxSteps, float mind){
        
    r=normalize(r); 
    vec3 p = o;
    vec3 uvw = vec3(0); 
    float d = 9999.0; 
    
    for (int i = 0; i < maxSteps; i++){ 
        d=mapScene(p,sceneID); 
        p+=d*r; 
        if(d<mind) break;
    } 
    vec2 uv = xy_uvs(p); 
    return marchResult(p, uv, length(p-o), d, 1);  
}

marchResult marchThis(vec3 o, vec3 r, int sceneID, int maxSteps, float mind)
{
    
    r=normalize(r); 
    vec3 p = o;
    vec3 uvw = vec3(0); 
    float d = 9999.0; 
    #define MAX_STEPS 256 
    #define MIND_BG 0.001//0.01*(1+LFO[4])  
    
    for (int i = 0; i < maxSteps; i++){ 
        d=mapScene(p,sceneID); 
        p+=d*r; 
        if(d<mind) break;
    } 
    vec2 uv = uvs(p); 
    return marchResult(p, uv, length(p-o), d, 1);  
    
}