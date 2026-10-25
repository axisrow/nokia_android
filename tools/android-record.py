import socket,time,json,pathlib,sys
root=pathlib.Path(__file__).resolve().parents[1]
state=root/'build/android-record-timeline.json'
class Console:
 def __init__(self):
  self.s=socket.create_connection(('127.0.0.1',5554),timeout=20);self.read()
 def read(self):
  data=b''
  while not(data.endswith(b'OK\r\n') or b'KO:' in data):
   d=self.s.recv(8192)
   if not d:break
   data+=d
  return data.decode()
 def cmd(self,t):
  self.s.sendall((t+'\n').encode());r=self.read()
  if 'KO:' in r:raise RuntimeError(r)
  return r
 def tap(self,x,y,delay=2):
  self.cmd(f'event mouse {x} {y} 0 1');time.sleep(.12);self.cmd(f'event mouse {x} {y} 0 0');time.sleep(delay)
 def shot(self,name):self.cmd('screenrecord screenshot '+str(root/'build'/name))
c=Console()
def mark(name):
 j=json.loads(state.read_text());j['events'].append([name,round(time.time()-j['start'],3)]);state.write_text(json.dumps(j));print(name,j['events'][-1][1],flush=True)
stage=sys.argv[1]
if stage=='start':
 state.write_text(json.dumps({'start':time.time(),'events':[]}));c.cmd('screenrecord start --time-limit 180 '+str(root/'build/Nokia3310-android-raw.webm'));mark('app_info');time.sleep(3);mark('open_apk');c.tap(124,500,5);c.shot('record-open.png')
elif stage=='game':
 mark('snake_menu');c.tap(358,750,3);mark('snake_start');c.tap(358,750,4);c.tap(490,925,2);c.tap(345,1010,2);mark('snake_pause');c.tap(358,750,2);c.shot('record-snake.png')
elif stage=='sms':
 mark('sms_menu');c.tap(200,750,2);c.tap(538,750,2);c.tap(358,750,3);c.shot('record-sms.png');mark('keyboard_focus');c.tap(300,495,4);c.shot('record-keyboard.png')
elif stage=='type':
 mark('typing');c.cmd('event text Nokia!');time.sleep(3);c.shot('record-typed.png')
elif stage=='hide':
 mark('hide_keyboard');c.cmd('event send EV_KEY:KEY_BACK:1 EV_SYN:SYN_REPORT:0 EV_KEY:KEY_BACK:0 EV_SYN:SYN_REPORT:0');time.sleep(3);c.shot('record-hidden.png')
elif stage=='ring':
 mark('save_sms');c.tap(358,750,2);c.tap(200,750,2);c.tap(538,750,2);c.tap(358,750,3);mark('ring_play');c.tap(358,750,1);c.shot('record-ring-playing.png');time.sleep(4);mark('ring_replay');c.tap(358,750,1);c.shot('record-ring-replay.png');time.sleep(4)
elif stage=='stop':
 mark('end');c.cmd('screenrecord stop');c.shot('record-end.png')
