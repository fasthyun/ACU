# for python3
# test sample 
_b1=b'\x020001,01MN,20231223170800,-3.8,-3.7,-3.8,52.1,52.7,51.7,1024.8,1024.8,1024.8,0.0,0.0,0.2,0.0,0.0,92.9,84.6,15.0\x03'
_b2=b'\x02-0.5,-15.6,0.0\x03\r\n'


from socketserver import TCPServer,BaseRequestHandler
from datetime import datetime
import socket
import select
from queue import Queue

def parse_KWEATHER(_bytes):    
    if _bytes[0] == 0x02 and _bytes[-1] == 0x03:            
        _list=_bytes[1:-1].decode().split(',')
        if len(_list) == 20: # 01MN
            print("DEBUG: 20 field found Type=", _list[1])
            _dict={
            '_id' :_list[0],
            '_type' :_list[1],
            'datetime':datetime.strptime(_list[2],"%Y%m%d%H%M%S"),
            'temp_now' : _list[3],
            'temp2' : _list[4],
            'temp3' : _list[5],
            'humidity':_list[6],
            'hum2' : _list[7],
            'hum3' : _list[8],
            'press1' :_list[9],
            'press2' : _list[10],
            'press3' : _list[11],
            'rainfall' : _list[12],
            'snowfall' : _list[13],
            'wind_speed_x' : _list[14],
            'wind_speed' : _list[15],
            '_none4' : _list[16],
            'wind_direction_x' : _list[17],
            'wind_direction' :_list[18],
            '_voltage': _list[19]}
            return _dict
        elif len(_list) == 11 : # 10SE                
            print("DEBUG: 11 field found Type=", _list[1])
            _dict={
            '_id' :_list[0],
            '_type' :_list[1],
            'datetime':datetime.strptime(_list[2],"%Y%m%d%H%M%S"),
            'temp_now' : _list[3],
            'humidity':_list[4],
            'pressure' :_list[5],
            'rainfall' : _list[6],
            'snowfall' : _list[7],   
            'wind_speed' : _list[8],  
            'wind_direction' :_list[9],
            '_voltage': _list[10]}
            return _dict        
        if len(_list) == 3:
            _dict={}
            print("DEBUG: 3 field found ",_bytes) 
            _dict={
            'temp_high_day' :_list[0],
            'temp_low_day' :_list[1],               
            'rainfall_yesterday' : _list[2]}
            return _dict
        else:
            print("DEBUG: unknown length frame =",len(_list),_bytes)
    
    print("unknown data =",_bytes)
    return {}

def parse_ACU_rx(_bytes):  
    _str=_bytes.decode('ascii')
    _list=_str.split(',')
    #print("DEBUG: 20 field found Type=", _list[1])    
    if len(_list)== 78 :
         _dict={
            '_' :_list[0], # 179.8225
            '_?' :_list[1], # C
            '_' :_list[0], # 46.6954
            '??': _list[3], # 0004000000301100030000050005000',
            '?' : _list[4], # 1
            '?' : _list[5], # 0
            '?' : _list[6], # 0
            '_' : _list[7], # 179.8225
            '_' : _list[8], #46.6954
            '?' : _list[9], #C
            '???' : _list[10], # 0
            '???' : _list[11], # 0.00
            '???' : _list[12], # 0.00
            '???' : _list[13], # -0.00
            '???' : _list[14], # 0.00
            '?' : _list[15], # -16.54
            '_db' : _list[16], # -91.54 db !!!
            'wind_direction_x' : _list[17],
            'wind_direction' :_list[18],
            '_voltage': _list[19]
            }
         return _dict
  
    
class HandleClass(BaseRequestHandler):    
    def setup(self):
        pass
    def handle(self):
        sock=self.request 
        _data=sock.recv(1024)
        self.server.put(_data)    
        print("DEBUG: transfered from : ", self.client_address,len(_data))       
        while True:
            _frame = self.server.getFrame()
            print("DEBUG: _frame=",_frame)
            if _frame is not None:
                self.server.que.put(_frame)
            else:
                break 
        
    def finish(self):
        print("DEBUG: HandleClass() finished()")

class Client:    
    def __init__(self):
        self._socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setblocking(False)
        #s.sendall(b'Hello, world')
        #data = s.recv(1024)
        self.isConnected = False
        self.que=Queue() # temporaly!!!
        
    def connect(self,host,port): 
        try :
            error=self._socket.connect((host, port))  
        #except  EINPROGRESS
        except InterruptedError :
            print("InteruptedError!!")
        except BlockingIOError as e :
            print("BlockingIOError...",e)
        except Exception as e :
            print("msg=",e)
        pass
    
    def onConnected(self):
        self._socket.send(b'hello?') 
        pass
    
    def handle(self):
        _list=[self._socket]
        readable, writeable, exceptions = select.select(_list, _list, _list, 1000)
        
        for fd  in readable:
            if fd == self._socket: 
                buf =self._socket.recv(1024) # ConnectionRefusedError
                if len(buf) !=0:
                    print("read= ", buf) 
        for fd  in writeable:
            if fd == self._socket:                
                if self.isConnected == False:
                    self.isConnected = True
                    print("Connected !!! ")#,self._socket.recv(1024)) 
                    self.onConnected()
                else:
                    pass
                    
        for fd  in exceptions:
            print("exception!!! "); 
            
        pass

"""    
import selectors
import socket

sel = selectors.DefaultSelector()

def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    data = conn.recv(1000)  # Should be ready
    if data:
        print('echoing', repr(data), 'to', conn)
        conn.send(data)  # Hope it won't block
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()

sock = socket.socket()
sock.bind(('localhost', 1234))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
        
""" 
import time
if __name__ =="__main__" :    
    #c=parse_KWEATHER(_b1)
    #print(c)
    #c=parse_KWEATHER(_b2)
    #print(c)
    client=Client()
    client.connect("127.0.0.1",2000)
    while True:
        client.handle()
        time.sleep(0.1)
    
    pass
print("__pacakge__",__package__)
