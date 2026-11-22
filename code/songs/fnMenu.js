{bpm:96,steps:64,play(i,t){ // chill lobby: Fmaj7 Em7 Dm7 Cmaj7, warm keys, laid-back beat
   const bar=Math.floor(i/16),s=i%16;const ch=[[53,57,60,64],[52,55,59,62],[50,53,57,60],[48,52,55,59]][bar],r=ch[0];
   if(s===0||s===7)ch.forEach((n,k)=>{tone({t,n:n+12,type:"sine",dur:s?.9:1.4,vol:.045,att:.01,bus:musBus});tone({t,n:n+24,type:"triangle",dur:.25,vol:.012,bus:musBus})});
   if(s===0||s===10)tone({t,n:r-12,type:"sine",dur:.5,vol:.28,bus:musBus});
   if(s===0||s===6||s===10)tone({t,f:120,slide:45,type:"sine",dur:.25,vol:.4,bus:musBus});
   if(s===4||s===12)noise({t,dur:.2,vol:.1,type:"bandpass",freq:1400,q:.7,bus:musBus});
   if(s%2===0)noise({t:t+(s%4===2?.04:0),dur:.03,vol:.035,freq:8000,bus:musBus});
   const mel={1:[[0,76],[3,79],[6,81],[10,79],[12,76]],3:[[0,74],[3,76],[6,79],[8,76],[11,72]]}[bar];
   if(mel)mel.forEach(([q,n])=>{if(q===s)tone({t,n,type:"triangle",dur:.35,vol:.06,bus:musBus})});
 }}