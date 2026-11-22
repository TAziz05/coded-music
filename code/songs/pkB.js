{bpm:120,steps:64,play(i,t){ // Battle B, "legendary": slow, heavy, ominous (Dm Bb Gm A)
   const bar=Math.floor(i/16),s=i%16;
   const mel=[[74,0,0,0,77,0,76,0],[74,0,72,0,70,0,0,0],[70,0,72,74,75,0,74,72],[73,0,0,0,76,0,79,0]][bar];
   if(s%2===0){const n=mel[s/2];if(n){const len=(mel[s/2+1]===0?(mel[s/2+2]===0?3:2):1)*.25;tone({t,n,type:"pulse",dur:len,vol:.08,bus:musBus});tone({t,n:n-12,type:"pulse12",dur:len,vol:.03,bus:musBus})}}
   const root=[38,34,43,45][bar];if(s%2===0)tone({t,n:root-12+(s%4===2?12:0),type:"triangle",dur:.2,vol:.24,bus:musBus});
   const tri=[[62,65,69],[58,62,65],[55,58,62],[57,61,64]][bar];tone({t,n:tri[s%3]+12,type:"pulse12",dur:.05,vol:.018,bus:musBus});
   if(s%8===0)tone({t,f:110,slide:40,type:"triangle",dur:.18,vol:.35,bus:musBus});
   if(s%8===4)noise({t,dur:.16,vol:.15,type:"highpass",freq:1500,bus:musBus});
   if(s%4===2)noise({t,dur:.02,vol:.04,freq:9000,bus:musBus});
   if(bar===3&&s>=8&&s%2===0)tone({t,f:180-s*6,slide:70,type:"triangle",dur:.12,vol:.25,bus:musBus});
 }}