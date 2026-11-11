"""Original loop for stage 2 (Baghdad): Hijaz mode on D, 10/8 jorjina-style pulse, plucked oud-like lead."""
import numpy as np, wave, os, subprocess
SR=44100; E8=0.185
N={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def f(n):
    if n=='.': return 0
    acc=1 if '#' in n else (-1 if 'b' in n else 0)
    return 440*2**((N[n[0]]+12*(int(n[-1])+1)+acc-69)/12)
def pluck(freq,dur,vol):
    t=np.arange(int(SR*dur))/SR
    if freq==0: return np.zeros(len(t))
    w=sum(np.sin(2*np.pi*freq*k*t*(1+0.0008*k))/k**1.25 for k in range(1,9))
    w+=0.5*sum(np.sin(2*np.pi*freq*1.006*k*t)/k**1.4 for k in range(1,6))   # double course
    env=np.minimum(1,t/0.003)*np.exp(-t*4.2)*np.minimum(1,(dur-t)/0.02)
    return w*env*vol
def trem(freq,dur,vol):
    t=np.arange(int(SR*dur))/SR; out=np.zeros(len(t)); step=0.062
    for i in range(int(dur/step)):
        p=pluck(freq,step*1.6,vol*(0.75 if i%2 else 1)); a=int(i*step*SR); out[a:a+len(p)]+=p[:len(out)-a]
    return out
M=[[('D5',3),('Eb5',2),('F#5',2),('G5',3)],[('A5',3),('G5',2),('F#5',2),('Eb5',3)],[('F#5',3),('G5',2),('A5',2),('Bb5',3)],[('A5',5),('G5',2),('F#5',3)],
   [('D5',3),('F#5',2),('A5',2),('D6',3)],[('C6',3),('Bb5',2),('A5',2),('G5',3)],[('F#5',3),('G5',2),('Eb5',2),('F#5',3)],[('D5',7),('.',3)],
   [('A5',2),('A5',1),('Bb5',2),('C6',2),('D6',3)],[('C6',3),('Bb5',2),('A5',2),('Bb5',3)],[('A5',3),('G5',2),('F#5',2),('G5',3)],[('A5',6),('.',1),('A5',1),('Bb5',1),('A5',1)],
   [('G5',3),('F#5',2),('Eb5',2),('D5',3)],[('Eb5',3),('F#5',2),('G5',2),('A5',3)],[('G5',2),('F#5',1),('Eb5',2),('F#5',2),('Eb5',3)],[('D5',8),('.',2)]]
bass=['D','D','D','D','D','G','D','D','A','G','D','A','G','C','D','D']
BN={'D':'D3','G':'G2','A':'A2','C':'C3'}
total=int(SR*E8*10*16); mix=np.zeros(total+SR)
def put(sig,at):
    i=int(at*SR); n=min(len(sig),len(mix)-i); mix[i:i+n]+=sig[:n]
rng=np.random.default_rng(2)
for b,bar in enumerate(M):
    assert sum(d for _,d in bar)==10,b
    t=b*10*E8
    for n,d in bar:
        put((trem if d>=5 else pluck)(f(n),d*E8*(1 if d>=5 else 1.5),0.20),t)
        if d>=3 and n!='.': put(pluck(f(n)/2,d*E8,0.07),t)
        t+=d*E8
    for e in range(10):
        at=(b*10+e)*E8; tt=np.arange(int(SR*0.16))/SR
        if e in (0,5): put(np.sin(2*np.pi*(95*np.exp(-tt*18)+62)*tt)*np.exp(-tt*16)*0.55,at)              # dum
        if e in (3,7,8): put((rng.uniform(-1,1,len(tt))*0.5+np.sin(2*np.pi*420*tt))*np.exp(-tt*55)*0.20,at)   # tek
        if e in (2,9): put(rng.uniform(-1,1,len(tt))*np.exp(-tt*110)*0.07,at)                                # ka
        if e in (0,3,5,7): put(pluck(f(BN[bass[b]])*(1.5 if e==7 else 1),E8*2.2,0.22),at)
    put(np.sin(2*np.pi*f('D3')*np.arange(int(SR*E8*10))/SR)*0.035,b*10*E8)
mix=mix[:total]; mix=np.tanh(mix*1.25)*0.8
out=os.path.join(os.path.dirname(__file__),'..','app','assets','stage2')
with wave.open('/tmp/m2.wav','wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg','-y','-loglevel','error','-i','/tmp/m2.wav','-b:a','192k',out+'/music.mp3'],check=True)
print('music2 ok',total/SR)
