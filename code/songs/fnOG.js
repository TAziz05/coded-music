{bpm:116,steps:128,play(i,t){ // OG-style lobby: bouncy drums, wobbly synth bass, orchestral stabs, mallet ostinato, horn tune (Gm Eb Bb F)
   const bar=Math.floor(i/16)%4,half=Math.floor(i/64),s=i%16,M=musBus;
   const roots=[43,39,46,41],r=roots[bar],ch=[[67,70,74],[67,70,75],[70,74,77],[69,72,77]][bar];
   if([0,7,8,10].includes(s))tone({t,f:150,slide:44,type:"sine",dur:.24,vol:.55,bus:M});
   if(s===4||s===12){noise({t,dur:.14,vol:.18,type:"bandpass",freq:1900,q:.9,bus:M});tone({t,f:210,slide:150,type:"triangle",dur:.08,vol:.18,bus:M})}
   if(s%2===0)noise({t,dur:.03,vol:.045,freq:8500,bus:M});if(s%4===2)noise({t,dur:.1,vol:.04,freq:7000,bus:M});
   if([0,3,6,8,11,14].includes(s)){const a=A,s0=a.currentTime+t,o=a.createOscillator(),fl=a.createBiquadFilter(),g=a.createGain();o.type="sawtooth";o.frequency.value=hz(r-12+(s===6||s===14?12:0));
     fl.type="lowpass";fl.Q.value=6;fl.frequency.setValueAtTime(200,s0);fl.frequency.linearRampToValueAtTime(1300,s0+.06);fl.frequency.exponentialRampToValueAtTime(250,s0+.2);
     g.gain.setValueAtTime(.0001,s0);g.gain.linearRampToValueAtTime(.16,s0+.004);g.gain.exponentialRampToValueAtTime(.0001,s0+.22);o.connect(fl);fl.connect(g);g.connect(M);o.start(s0);o.stop(s0+.26)}
   if((s===0&&bar%2===0)||(s===6&&bar%2===1)){ch.forEach(n=>brass({t,n,dur:.14,vol:.03,bus:M}));ch.forEach(n=>tone({t,n:n+12,type:"sawtooth",dur:.12,vol:.014,cut:3000,bus:M}))}
   if(s%2===0){const n=[...ch,ch[1]+12,ch[2]+12,ch[1]+12,ch[2],ch[1]][(s/2)%8]+12;tone({t,n,type:"sine",dur:.3,vol:.05,att:.002,bus:M});tone({t,f:hz(n)*4,type:"sine",dur:.05,vol:.012,att:.001,bus:M})}
   if(half===1){const mel=[[67,0,70,74,0,72,70,0],[70,0,67,63,0,67,70,72],[74,0,77,74,72,70,0,69],[72,0,0,69,0,65,0,0]][bar];
     if(s%2===0){const n=mel[s/2];if(n){const len=(mel[s/2+1]===0?2:1)*.26;brass({t,n,dur:len,vol:.045,bus:M});brass({t,n:n-12,dur:len,vol:.025,bus:M})}}}
   if(bar===3&&half===1&&s===12)noise({t,dur:.6,vol:.06,freq:5000,bus:M});
 }}