import socket,sys
with socket.create_connection(('127.0.0.1',5554), timeout=10) as s:
 s.settimeout(10)
 def read():
  result=b''
  while not(result.endswith(b'OK\r\n') or b'KO:' in result):
   d=s.recv(8192)
   if not d:break
   result+=d
  return result.decode()
 read()
 s.sendall((' '.join(sys.argv[1:])+'\n').encode())
 print(read())
