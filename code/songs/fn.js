{bpm:128,steps:64,play(i,t){ // D minor epic lobby: Dm Bb F C, pumping pads, plucky arp, brass stabs
   const bar=Math.floor(i/16),s=i%16,a=A,at=a.currentTime+t;
   const roots=[50,46,53,48],tri=[[62,65,69],[58,62,65],[60,65,69],[60,64,67]][bar],r=roots[bar];
   if(!SONGS.pad){SONGS.pad=a.createGain();SONGS.pad.connect(musBus)}
   const pad=SONGS.pad.gain;
   if(s%4===0){tone({t,f:160,slide:42,type:"sine",dur:.26,vol:.6,bus:musBus});pad.setTargetAtTime(.3,at,.008);pad.setTargetAtTime(1,at+.03,.07)}
   if(s===4||s===12){noise({t,dur:.16,vol:.16,type:"bandpass",freq:1500,q:.7,bus:musBus});noise({t,dur:.08,vol:.08,freq:5000,bus:musBus})}
   if(s%2===1)noise({t,dur:.03,vol:.05,freq:9000,bus:musBus});
   if(s===0)tri.forEach((n,k)=>[-8,8].forEach(dt=>tone({t,n,type:"sawtooth",dur:1.8,vol:.03,cut:1600,att:.2,detune:dt+k,bus:SONGS.pad})));
   if(s%2===0)tone({t,n:r-24,type:"sine",dur:.2,vol:.3,bus:SONGS.pad});
   const arp=[0,1,2,1,2,0,1,2,0,2,1,2,0,1,2,1];tone({t,n:tri[arp[s]]+12,type:"square",dur:.09,vol:.035,cut:2600,bus:musBus});
   if(s===0||(s===10&&bar%2===1))brass({t,n:tri[2]+(s?2:0),dur:s?.18:.3,vol:.05,bus:musBus});
   const hook=[[0,74],[2,77],[4,81],[7,79],[8,77],[11,74],[12,76]];
   if(bar===3)hook.forEach(([q,n])=>{if(q===s)brass({t,n,dur:.16,vol:.04,bus:musBus})});
 }}