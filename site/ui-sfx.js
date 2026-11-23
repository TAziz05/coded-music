/* Button sound effects for the Coded Music site and Loop Lab, synthesized with the Web Audio API (no audio files).
   UISFX.play('click' | 'tap' | 'open' | 'close' | 'play' | 'pause' | 'on' | 'off' | 'success' | 'error' | 'whoosh' | 'sparkle')
   UISFX.set(true/false) turns them on or off (remembered on this device). */
window.UISFX = (() => {
  let c = null, on = true;
  try { on = localStorage.getItem('uisfx') !== 'off'; } catch (e) {}
  const ctx = () => { if (!c) c = new (window.AudioContext || window.webkitAudioContext)(); if (c.state === 'suspended') c.resume(); return c; };
  function tone(f, t, d, type = 'triangle', v = .05, f2 = null) {
    const a = ctx(), T = a.currentTime + t, o = a.createOscillator(), g = a.createGain(), lp = a.createBiquadFilter();
    lp.type = 'lowpass'; lp.frequency.value = 4000; o.type = type; o.frequency.setValueAtTime(f, T);
    if (f2) o.frequency.exponentialRampToValueAtTime(f2, T + d);
    g.gain.setValueAtTime(0, T); g.gain.linearRampToValueAtTime(v, T + .004); g.gain.exponentialRampToValueAtTime(.0001, T + d);
    o.connect(lp).connect(g).connect(a.destination); o.start(T); o.stop(T + d + .03);
  }
  function noise(t, d, f0, f1, v = .05) {
    const a = ctx(), T = a.currentTime + t, n = Math.ceil(d * a.sampleRate), b = a.createBuffer(1, n, a.sampleRate), x = b.getChannelData(0);
    for (let i = 0; i < n; i++) x[i] = Math.random() * 2 - 1;
    const s = a.createBufferSource(), bp = a.createBiquadFilter(), g = a.createGain(); s.buffer = b; bp.type = 'bandpass'; bp.Q.value = 2;
    bp.frequency.setValueAtTime(f0, T); bp.frequency.exponentialRampToValueAtTime(f1, T + d);
    g.gain.setValueAtTime(0, T); g.gain.linearRampToValueAtTime(v, T + d * .3); g.gain.exponentialRampToValueAtTime(.0001, T + d);
    s.connect(bp).connect(g).connect(a.destination); s.start(T);
  }
  const SFX = {
    click: () => tone(1500, 0, .035, 'square', .025),
    tap: () => tone(880, 0, .06, 'triangle', .06),
    open: () => { tone(660, 0, .07, 'triangle', .055); tone(990, .055, .1, 'triangle', .055); },
    close: () => { tone(880, 0, .06, 'triangle', .05); tone(587, .05, .09, 'triangle', .05); },
    play: () => tone(520, 0, .13, 'sine', .08, 1040),
    pause: () => tone(780, 0, .11, 'sine', .07, 390),
    on: () => { tone(700, 0, .05, 'square', .025); tone(1050, .05, .07, 'square', .025); },
    off: () => { tone(1050, 0, .05, 'square', .025); tone(700, .05, .07, 'square', .025); },
    success: () => [523, 659, 784, 1047].forEach((f, i) => tone(f, i * .06, .14, 'triangle', .055)),
    error: () => tone(240, 0, .2, 'sawtooth', .035, 150),
    whoosh: () => noise(0, .35, 400, 4000, .06),
    sparkle: () => [1319, 1568, 1976, 2637].forEach((f, i) => tone(f, i * .045, .12, 'sine', .035)),
  };
  return {
    play(name) { if (on && SFX[name]) try { SFX[name](); } catch (e) {} },
    get on() { return on; },
    set(v) { on = !!v; try { localStorage.setItem('uisfx', on ? 'on' : 'off'); } catch (e) {} }
  };
})();
