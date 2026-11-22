{bpm:140,steps:64,play(i,t){ // route theme, now the menu song: C Am F G chiptune
   const bar=Math.floor(i/16),s=i%16;
   const mel=[[76,79,84,0,83,79,76,79],[81,0,84,81,76,0,72,76],[77,81,84,86,84,81,77,0],[79,83,86,0,84,83,79,74]][bar];
   if(s%2===0){const n=mel[s/2];if(n)tone({t,n,dur:.17,vol:.07,bus:musBus})}
   const bass=[48,45,41,43][bar];
   if(s%2===0)tone({t,n:bass+(s%4===2?12:0),type:"triangle",dur:.18,vol:.22,bus:musBus});
   if(s%4===0)tone({t,f:120,slide:50,type:"triangle",dur:.08,vol:.25,bus:musBus});
   if(s===4||s===12)noise({t,dur:.08,vol:.1,type:"highpass",freq:2500,bus:musBus});
   if(s%2===1)noise({t,dur:.025,vol:.04,freq:9000,bus:musBus});
 }}