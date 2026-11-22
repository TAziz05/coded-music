{bpm:166,steps:64,play(i,t){ // battle theme for questions: Am F G E, driving and tense
   const bar=Math.floor(i/16),s=i%16;
   const mel=[[69,72,76,0,74,72,71,72],[77,0,76,74,72,0,69,72],[74,76,79,0,77,76,74,71],[76,0,80,0,83,0,80,76]][bar];
   if(s%2===0){const n=mel[s/2];if(n)tone({t,n,type:"pulse",dur:.13,vol:.075,bus:musBus})}
   const root=[45,41,43,40][bar];tone({t,n:root+(s%2?12:0),type:"triangle",dur:.08,vol:.2,bus:musBus});
   const tri=[[69,72,76],[65,69,72],[67,71,74],[64,68,71]][bar];tone({t,n:tri[s%3]+12,type:"pulse12",dur:.05,vol:.022,bus:musBus});
   if(s%4===0)tone({t,f:130,slide:45,type:"triangle",dur:.08,vol:.3,bus:musBus});
   if(s%8===4)noise({t,dur:.1,vol:.13,type:"highpass",freq:2000,bus:musBus});
   if(s%2===1)noise({t,dur:.02,vol:.04,freq:9000,bus:musBus});
   if(bar===3&&s>=12)noise({t,dur:.05,vol:.08,type:"highpass",freq:2500,bus:musBus});
 }}