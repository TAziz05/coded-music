{bpm:128,steps:64,play(i,t){ // Match OG-style: faster, driving version of the OG lobby feel (Dm Bb C A)
   const bar=Math.floor(i/16),s=i%16,M=musBus;const roots=[38,46,48,45],r=roots[bar],ch=[[62,65,69],[62,65,70],[64,67,72],[61,64,69]][bar];
   if(s%4===0||s===14)tone({t,f:150,slide:44,type:"sine",dur:.22,vol:.55,bus:M});
   if(s===4||s===12){noise({t,dur:.13,vol:.18,type:"bandpass",freq:1900,q:.9,bus:M});tone({t,f:220,slide:150,type:"triangle",dur:.07,vol:.16,bus:M})}
   noise({t,dur:.025,vol:s%2?.045:.025,freq:9000,bus:M});
   if(s%2===0||s===3||s===11){const a=A,s0=a.currentTime+t,o=a.createOscillator(),fl=a.createBiquadFilter(),g=a.createGain();o.type="sawtooth";o.frequency.value=hz(r-12+(s%4===2?12:0));
     fl.type="lowpass";fl.Q.value=6;fl.frequency.setValueAtTime(200,s0);fl.frequency.linearRampToValueAtTime(1500,s0+.05);fl.frequency.exponentialRampToValueAtTime(250,s0+.15);
     g.gain.setValueAtTime(.0001,s0);g.gain.linearRampToValueAtTime(.14,s0+.004);g.gain.exponentialRampToValueAtTime(.0001,s0+.16);o.connect(fl);fl.connect(g);g.connect(M);o.start(s0);o.stop(s0+.2)}
   if(s===0||s===10)ch.forEach(n=>brass({t,n,dur:.12,vol:.028,bus:M}));
   {const n=[...ch,ch[0]+12][s%4]+12;tone({t,n,type:"sine",dur:.12,vol:.035,att:.002,bus:M})}
   const mel=[[[0,74],[3,77],[6,81],[10,79],[12,77]],[[0,77],[3,74],[6,70],[10,74],[12,77]],[[0,79],[3,76],[6,72],[10,76],[12,79]],[[0,81],[6,85],[10,88]]][bar];
   mel.forEach(([q,n])=>{if(q===s){brass({t,n,dur:.22,vol:.04,bus:M});brass({t,n:n-12,dur:.22,vol:.022,bus:M})}});
   if(bar===3&&s>=12)noise({t,dur:.05,vol:.1,type:"bandpass",freq:1900,q:.9,bus:M});
 }}