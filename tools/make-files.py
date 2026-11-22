"""Turns the raw recordings from record.py into:
  loops/<song>.mp3   one seamless loop with 0.3 s of overlap on each side (loop from 0.3 s for exactly one loop length)
  songs/.../*.mp3    about 2-minute versions with a fade-out
Needs numpy and ffmpeg."""
import wave,numpy as np,json,subprocess,os
HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.join(HERE,"..");B=os.path.join(ROOT,"build")
m=json.load(open(os.path.join(B,"meta.json")));sr=44100;P=round(.3*sr);XF=round(.02*sr)
NAMES={"fnMenu":"drop-in-daily/Drop-In Daily - Lobby","fn":"drop-in-daily/Drop-In Daily - Match","fnOGm":"drop-in-daily/Drop-In Daily - Mythic Match (OG style)",
 "fnOG":"drop-in-daily/Drop-In Daily - Endless Summary (OG lobby style)","pkMenu":"daily-poke-catch/Daily Poke Catch - Route (Menus)",
 "pkB":"daily-poke-catch/Daily Poke Catch - Battle","pk":"daily-poke-catch/Daily Poke Catch - Mythic Battle","pkTown":"daily-poke-catch/Daily Poke Catch - Town (Endless Summary)"}
def mp3(x,path,stereo=False,rate="112k"):
    tmp=path+".wav"
    with wave.open(tmp,"wb") as o:o.setnchannels(1);o.setsampwidth(2);o.setframerate(sr);o.writeframes((np.clip(x,-1,1)*32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg","-v","error","-y","-i",tmp,"-ac","2" if stereo else "1","-b:a",rate,"-c:a","libmp3lame",path],check=True);os.remove(tmp)
info={}
for n,r in m.items():
    w=wave.open(os.path.join(B,f"{n}-raw.wav"));x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float64)/32767
    N=round(r["L"]*sr);C=x[P:P+N].copy();a=np.linspace(1,0,XF);C[:XF]=a*x[P+N:P+N+XF]+(1-a)*C[:XF]
    y=np.concatenate([C[-P:],C,C[:P]]);pk=np.abs(y).max();mp3(y/pk*.89,os.path.join(ROOT,"loops",f"{n}.mp3"))
    info[n]={"L":N/sr,"pad":.3,"gain":round(1/(r["f"]*.89/pk),5)}
    t=np.tile(C,int(np.ceil(124*sr/N)))[:124*sr]/pk*.89;t[:441]*=np.linspace(0,1,441);t[-5*sr:]*=np.linspace(1,0,5*sr)**1.5
    mp3(t,os.path.join(ROOT,"songs",NAMES[n]+".mp3"),True,"320k")
json.dump(info,open(os.path.join(ROOT,"loops","music.json"),"w"),indent=0)
