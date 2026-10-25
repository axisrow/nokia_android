import wave, math, struct
# Nokia Tune: the public-domain Gran Vals motif, synthesized as monophonic pulses.
notes=[(76,.16),(74,.16),(66,.32),(68,.32),(73,.16),(71,.16),(62,.32),(64,.32),(71,.16),(69,.16),(61,.32),(64,.32),(69,.64)]
rate=44100
samples=[]
for midi,duration in notes:
 for i in range(round(rate*duration)):
  t=i/rate; env=min(1,t/.006)*min(1,max(0,(duration-t-.025)/.015)); f=440*2**((midi-69)/12)
  value=(math.sin(2*math.pi*f*t)+.22*math.sin(6*math.pi*f*t))*env*.24
  samples.append(int(value*32767))
with wave.open('app/src/main/assets/tune.wav','wb') as w:
 w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(struct.pack('<'+'h'*len(samples),*samples))
