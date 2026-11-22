function pulse(d){pulse.c=pulse.c||{};if(pulse.c[d])return pulse.c[d];const N=32,re=new Float32Array(N),im=new Float32Array(N);for(let k=1;k<N;k++){re[k]=Math.sin(2*Math.PI*k*d)/(k*Math.PI);im[k]=(1-Math.cos(2*Math.PI*k*d))/(k*Math.PI)}return pulse.c[d]=ctx().createPeriodicWave(re,im)}
function tone({t=0,n,f,type="square",dur=.12,vol=.3,slide,bus=sfxBus,detune=0,att=.005,cut}){
  const a=ctx(),s=a.currentTime+t,o=a.createOscillator(),g=a.createGain();
  if(type.startsWith("pulse"))o.setPeriodicWave(pulse(type==="pulse"?.25:.125));else o.type=type;o.frequency.setValueAtTime(f||hz(n),s);o.detune.value=detune;
  if(slide)o.frequency.exponentialRampToValueAtTime(slide,s+dur);
  g.gain.setValueAtTime(0.0001,s);g.gain.exponentialRampToValueAtTime(vol,s+att);g.gain.exponentialRampToValueAtTime(0.0001,s+dur);
  let last=o; o.connect(g);
  if(cut){const fl=a.createBiquadFilter();fl.type="lowpass";fl.frequency.value=cut;g.connect(fl);last=fl}else last=g;
  last.connect(bus);o.start(s);o.stop(s+dur+.05);
}
function noise({t=0,dur=.1,vol=.25,type="highpass",freq=6000,sweep,bus=sfxBus,q=1}){
  const a=ctx(),s=a.currentTime+t,src=a.createBufferSource(),fl=a.createBiquadFilter(),g=a.createGain();
  src.buffer=noiseBuf;src.loop=true;fl.type=type;fl.frequency.setValueAtTime(freq,s);fl.Q.value=q;
  if(sweep)fl.frequency.exponentialRampToValueAtTime(sweep,s+dur);
  g.gain.setValueAtTime(0.0001,s);g.gain.linearRampToValueAtTime(vol,s+.002);g.gain.exponentialRampToValueAtTime(0.0001,s+dur);
  src.connect(fl);fl.connect(g);g.connect(bus);src.start(s,Math.random()*.8);src.stop(s+dur+.05);
}
function verb(){const a=ctx();if(verb.n)return verb.n;const len=a.sampleRate*1.5,b=a.createBuffer(2,len,a.sampleRate);
  for(let c=0;c<2;c++){const d=b.getChannelData(c);for(let i=0;i<len;i++)d[i]=(Math.random()*2-1)*Math.pow(1-i/len,3)}
  const cv=a.createConvolver();cv.buffer=b;const g=a.createGain();g.gain.value=.35;cv.connect(g);g.connect(master);
  const send=a.createGain();send.connect(sfxBus);send.connect(cv);return verb.n=send}
function brass({t=0,n,dur=.4,vol=.12,bus}){const a=ctx(),s=a.currentTime+t,out=bus||verb(),fl=a.createBiquadFilter(),g=a.createGain();
  fl.type="lowpass";fl.Q.value=2;fl.frequency.setValueAtTime(500,s);fl.frequency.linearRampToValueAtTime(3200,s+.06);fl.frequency.exponentialRampToValueAtTime(1400,s+dur);
  g.gain.setValueAtTime(.0001,s);g.gain.exponentialRampToValueAtTime(vol,s+.04);g.gain.setValueAtTime(vol,s+dur*.8);g.gain.exponentialRampToValueAtTime(.0001,s+dur+.15);
  const lfo=a.createOscillator(),lg=a.createGain();lfo.frequency.value=5.5;lg.gain.setValueAtTime(0,s);lg.gain.linearRampToValueAtTime(dur>.35?12:0,s+dur);lfo.connect(lg);
  [-9,0,9].forEach(dt=>{const o=a.createOscillator();o.type="sawtooth";o.frequency.value=hz(n);o.detune.value=dt;lg.connect(o.detune);o.connect(fl);o.start(s);o.stop(s+dur+.2)});
  lfo.start(s);lfo.stop(s+dur+.2);fl.connect(g);g.connect(out)}
function boom(t=0,vol=.5){tone({t,f:110,slide:48,type:"sine",dur:.7,vol,bus:verb()});noise({t,dur:.25,vol:.12,type:"lowpass",freq:300,bus:verb()})}
function aah({t=0,ns,dur=1,vol=.06}){const a=ctx(),s=a.currentTime+t,g=a.createGain(),out=verb();
  g.gain.setValueAtTime(.0001,s);g.gain.exponentialRampToValueAtTime(vol,s+dur*.4);g.gain.exponentialRampToValueAtTime(.0001,s+dur);
  const f1=a.createBiquadFilter();f1.type="bandpass";f1.frequency.value=750;f1.Q.value=5;const f2=a.createBiquadFilter();f2.type="bandpass";f2.frequency.value=1150;f2.Q.value=7;f1.connect(g);f2.connect(g);
  ns.forEach((n,k)=>[-6,6].forEach(dt=>{const o=a.createOscillator();o.type="sawtooth";o.frequency.value=hz(n);o.detune.value=dt+k;o.connect(f1);o.connect(f2);o.start(s);o.stop(s+dur+.05)}));
  g.connect(out)}
function fadeBus(start,len){const a=ctx(),g=a.createGain(),s0=a.currentTime;g.gain.setValueAtTime(1,s0+start);g.gain.linearRampToValueAtTime(.0001,s0+start+len);g.connect(verb());return g}
function pluck(t,n,vol=.14,dur=.3){tone({t,n,type:"triangle",dur,vol,att:.002,cut:2200,bus:verb()});tone({t,n:n+12,type:"sine",dur:dur*.4,vol:vol*.3,att:.002,bus:verb()})}
function mallet(t,n,vol=.14){tone({t,n,type:"sine",dur:.45,vol,att:.002,bus:verb()});tone({t,f:hz(n)*4,type:"sine",dur:.06,vol:vol*.35,att:.001})}
function glock(t,n,vol=.1){tone({t,n,type:"sine",dur:1.1,vol,att:.002,bus:verb()});tone({t,f:hz(n)*2.76,type:"sine",dur:.3,vol:vol*.25,att:.001,bus:verb()})}
function flute({t=0,n,dur=.3,vol=.08}){const a=ctx(),s0=a.currentTime+t,o=a.createOscillator(),g=a.createGain(),l=a.createOscillator(),lg=a.createGain();
  o.type="sine";o.frequency.value=hz(n);l.frequency.value=5.2;lg.gain.setValueAtTime(0,s0);lg.gain.linearRampToValueAtTime(dur>.3?10:3,s0+dur);l.connect(lg);lg.connect(o.detune);
  g.gain.setValueAtTime(.0001,s0);g.gain.exponentialRampToValueAtTime(vol,s0+.05);g.gain.setValueAtTime(vol,s0+dur*.8);g.gain.exponentialRampToValueAtTime(.0001,s0+dur+.1);
  o.connect(g);g.connect(verb());o.start(s0);l.start(s0);o.stop(s0+dur+.15);l.stop(s0+dur+.15);noise({t,dur:.06,vol:vol*.4,type:"bandpass",freq:hz(n)*2,q:3,bus:verb()})}
function horn({t=0,n,dur=.4,vol=.1}){const a=ctx(),s0=a.currentTime+t,fl=a.createBiquadFilter(),g=a.createGain();
  fl.type="lowpass";fl.Q.value=.7;fl.frequency.setValueAtTime(400,s0);fl.frequency.linearRampToValueAtTime(1500,s0+.08);fl.frequency.exponentialRampToValueAtTime(900,s0+dur);
  g.gain.setValueAtTime(.0001,s0);g.gain.exponentialRampToValueAtTime(vol,s0+.07);g.gain.setValueAtTime(vol,s0+dur*.85);g.gain.exponentialRampToValueAtTime(.0001,s0+dur+.2);
  [-5,5].forEach(dt=>{const o=a.createOscillator();o.type="sawtooth";o.frequency.value=hz(n);o.detune.value=dt;o.connect(fl);o.start(s0);o.stop(s0+dur+.25)});
  const o2=a.createOscillator();o2.type="triangle";o2.frequency.value=hz(n);o2.connect(fl);o2.start(s0);o2.stop(s0+dur+.25);fl.connect(g);g.connect(verb())}
function strings({t=0,ns,dur=1,vol=.03}){ns.forEach((n,k)=>[-10,10].forEach(dt=>tone({t,n,type:"sawtooth",dur,vol,att:.25,cut:1800,detune:dt+k*2,bus:verb()})))}
function swell(t,dur,vol=.12){const a=ctx(),s0=a.currentTime+t,src=a.createBufferSource(),fl=a.createBiquadFilter(),g=a.createGain();src.buffer=noiseBuf;src.loop=true;fl.type="highpass";fl.frequency.value=5000;
  g.gain.setValueAtTime(.0001,s0);g.gain.exponentialRampToValueAtTime(vol,s0+dur);g.gain.exponentialRampToValueAtTime(.0001,s0+dur+.8);src.connect(fl);fl.connect(g);g.connect(verb());src.start(s0);src.stop(s0+dur+.9)}
function roll(t,dur,vol=.35){for(let k=0;k*.05<dur;k++)tone({t:t+k*.05,f:98,slide:80,type:"sine",dur:.12,vol:vol*(.3+.7*k*.05/dur),att:.003})}
function harp(t,ns,gap=.035,vol=.1){ns.forEach((n,i)=>pluck(t+i*gap,n,vol,.6))}
function wub(t,n,{vol=.14,dur=.22,peak=1400,type="sawtooth",slide}={}){const a=ctx(),s0=a.currentTime+t,o=a.createOscillator(),fl=a.createBiquadFilter(),g=a.createGain();o.type=type;o.frequency.setValueAtTime(hz(n),s0);if(slide)o.frequency.exponentialRampToValueAtTime(hz(slide),s0+dur);
  fl.type="lowpass";fl.Q.value=7;fl.frequency.setValueAtTime(180,s0);fl.frequency.linearRampToValueAtTime(peak,s0+Math.min(.07,dur*.4));fl.frequency.exponentialRampToValueAtTime(200,s0+dur);
  g.gain.setValueAtTime(.0001,s0);g.gain.linearRampToValueAtTime(vol,s0+.004);g.gain.setValueAtTime(vol,s0+dur*.7);g.gain.exponentialRampToValueAtTime(.0001,s0+dur);o.connect(fl);fl.connect(g);g.connect(sfxBus);o.start(s0);o.stop(s0+dur+.05)}
function stab(t,ns,vol=.05,dur=.16){ns.forEach(n=>{brass({t,n,dur,vol});tone({t,n:n+12,type:"sawtooth",dur:dur*.8,vol:vol*.35,cut:3200,bus:verb()})})}
function snare(t,vol=.2){noise({t,dur:.13,vol,type:"bandpass",freq:1900,q:.9,bus:verb()});tone({t,f:220,slide:150,type:"triangle",dur:.07,vol:vol*.8})}
function riser(t,dur,vol=.12){const a=ctx(),s0=a.currentTime+t,src=a.createBufferSource(),fl=a.createBiquadFilter(),g=a.createGain();src.buffer=noiseBuf;src.loop=true;fl.type="bandpass";fl.Q.value=3;fl.frequency.setValueAtTime(300,s0);fl.frequency.exponentialRampToValueAtTime(7000,s0+dur);
  g.gain.setValueAtTime(.0001,s0);g.gain.exponentialRampToValueAtTime(vol,s0+dur);g.gain.exponentialRampToValueAtTime(.0001,s0+dur+.05);src.connect(fl);fl.connect(g);g.connect(sfxBus);src.start(s0);src.stop(s0+dur+.1)}