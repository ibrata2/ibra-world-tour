"""Original chiptune loop for stage 1 (composed for this game). 16 bars, 152 bpm, C major."""
import numpy as np, wave, os, subprocess
SR=44100; BPM=152; E8=60/BPM/2
N={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def f(n):
    if n=='.': return 0
    return 440*2**((N[n[0]]+12*(int(n[-1])+1)+(1 if '#' in n else 0)-69)/12)
def tone(freq,dur,kind,vol):
    t=np.arange(int(SR*dur))/SR
    if freq==0: return np.zeros(len(t))
    if kind=='sq': w=np.sign(np.sin(2*np.pi*freq*t)+0.5)*0.5+0.25*np.sign(np.sin(2*np.pi*freq*2*t))*0
    elif kind=='pulse': w=np.where((t*freq)%1<0.25,1.0,-1.0)
    else: w=2*np.abs(2*((t*freq)%1)-1)-1
    env=np.minimum(1,t/0.004)*np.exp(-t*(2.2 if kind!='tri' else 0.6))
    rel=np.minimum(1,(dur-t)/0.02)
    return w*env*rel*vol
# melody: (note, eighths)
A=[('E5',1),('G5',1),('C6',2),('B5',1),('G5',1),('E5',2),
   ('A5',1),('C6',1),('E6',2),('D6',1),('C6',1),('A5',2),
   ('F5',1),('A5',1),('C6',1),('F6',1),('E6',2),('D6',1),('C6',1),
   ('D6',2),('B5',1),('G5',1),('A5',1),('B5',1),('D6',2),
   ('E5',1),('G5',1),('C6',2),('B5',1),('G5',1),('E6',2),
   ('A5',1),('C6',1),('E6',2),('G6',1),('E6',1),('C6',2),
   ('F6',1),('E6',1),('D6',1),('C6',1),('B5',1),('D6',1),('G5',1),('B5',1),
   ('C6',3),('G5',1),('C6',2),('.',2)]
B=[('A5',2),('F5',1),('A5',1),('C6',2),('A5',2),
   ('B5',2),('G5',1),('B5',1),('D6',2),('B5',2),
   ('G5',1),('B5',1),('E6',2),('D6',1),('B5',1),('G5',2),
   ('A5',1),('.',1),('A5',1),('C6',1),('E6',2),('C6',2),
   ('F5',1),('A5',1),('C6',1),('A5',1),('F6',2),('E6',1),('D6',1),
   ('D6',1),('B5',1),('G5',1),('B5',1),('D6',1),('G6',1),('F6',1),('D6',1),
   ('E6',2),('C6',1),('G5',1),('E6',1),('D6',1),('C6',2),
   ('C6',4),('.',2),('G5',1),('G5',1)]
chords=['C','A','F','G','C','A','FG','C','F','G','E','A','F','G','C','C']
root={'C':'C3','A':'A2','F':'F2','G':'G2','E':'E3'}
third={'C':('E4','G4'),'A':('C4','E4'),'F':('A3','C4'),'G':('B3','D4'),'E':('G3','B3')}
total=int(SR*E8*8*16)+SR
mix=np.zeros(total)
def put(sig,at):
    i=int(at*SR); mix[i:i+len(sig)]+=sig[:max(0,total-i)]
t=0
for n,d in A+B:
    put(tone(f(n),d*E8*0.95,'pulse',0.20),t); t+=d*E8
assert abs(t-E8*8*16)<1e-6, t/(E8*8)
rng=np.random.default_rng(1)
for bar,ch in enumerate(chords):
    for e in range(8):
        c=ch[0] if len(ch)==1 or e<4 else ch[1]
        at=(bar*8+e)*E8
        bn=root[c] if e%2==0 else root[c][0]+str(int(root[c][1])+1)
        put(tone(f(bn),E8*0.9,'tri',0.34),at)
        if e%2==1:
            for hn in third[c]: put(tone(f(hn),E8*0.5,'sq',0.07),at)
        # drums: kick on 0,4 ; snare on 2,6 ; hat every eighth
        tt=np.arange(int(SR*0.09))/SR
        if e in (0,4): put(np.sin(2*np.pi*(120*np.exp(-tt*30)+45)*tt)*np.exp(-tt*28)*0.5,at)
        if e in (2,6): put(rng.uniform(-1,1,len(tt))*np.exp(-tt*38)*0.22,at)
        put(rng.uniform(-1,1,len(tt))*np.exp(-tt*120)*0.06,at)
mix=mix[:int(SR*E8*8*16)]
mix=np.tanh(mix*1.3)*0.8
out=os.path.join(os.path.dirname(__file__),'..','app','assets','stage1')
with wave.open(out+'/music.wav','wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',out+'/music.wav','-b:a','192k',out+'/music.mp3'],check=True)
print('music ok', len(mix)/SR,'s')
