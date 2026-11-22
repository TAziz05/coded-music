{bpm:104,steps:64,play(i,t){ // cozy town tune for the Endless screen: F Dm Bb C
   const bar=Math.floor(i/16),s=i%16;
   const mel=[[72,0,69,72,77,0,76,74],[74,0,72,69,65,0,0,0],[70,74,77,0,79,77,74,72],[72,0,74,76,79,0,0,0]][bar];
   if(s%2===0){const n=mel[s/2];if(n)tone({t,n,type:"pulse",dur:.24,vol:.07,bus:musBus})}
   const root=[41,38,46,48][bar];if(s%4===0)tone({t,n:root+(s%8===4?7:0),type:"triangle",dur:.3,vol:.22,bus:musBus});
   const tri=[[65,69,72],[62,65,69],[62,65,70],[64,67,72]][bar];if(s%4===2)tri.forEach(n=>tone({t,n,type:"pulse12",dur:.12,vol:.02,bus:musBus}));
   if(s%2===0)noise({t,dur:.02,vol:.025,freq:9000,bus:musBus});
 }}