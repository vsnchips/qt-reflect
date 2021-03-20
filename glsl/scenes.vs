
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
