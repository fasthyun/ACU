# for python3
# test sample 
_b1=b'\x020001,01MN,20231223170800,-3.8,-3.7,-3.8,52.1,52.7,51.7,1024.8,1024.8,1024.8,0.0,0.0,0.2,0.0,0.0,92.9,84.6,15.0\x03'
_b2=b'\x02-0.5,-15.6,0.0\x03\r\n'

_b3=b"""179.8225,C,46.6954,0004000000301100030000050005000,1,0,0,179.8225,46.6954,C, 
 0,0,0.00,0.00,-0.00,-0.00,-16.54,-91.54,-1,2,-1,0,"None",0,"Stop             ",0,
"None",0,30,"None",0,"None",0,30,"None",0,"None",0,1,"Config 1",68,"128E COS-2526 3.4006",
3.400000,2,1,00:00:00:001:1970,9.0,09:00:00:001:1970,"13M #1",
180.4199,180.4199,0,0.00,50,"Stop   ",0,"None",
0,0.0000,0.0000,0.0000,0.0000,1,0,90.000,350.000,90.000,0,4,0,11,0,1,
0.3455,-0.22,127.44,4,"C1 LHCP"\x0d\x0a"""
   
from socketserver import TCPServer,BaseRequestHandler
from datetime import datetime
import socket
import select
from queue import Queue


class HandleClass(BaseRequestHandler):    
    def setup(self):
        print("DEBUG: setup()") # 초기화
        pass
    def handle(self):
        sock=self.request 
        _data=sock.recv(1024)
        ###self.server.put(_data) 
        print("DEBUG: transfered from : ", self.client_address,len(_data),_data)               
        return 
        while True:
            _frame = self.server.getFrame()
            print("DEBUG: _frame=",_frame)
            if _frame is not None:
                self.server.que.put(_frame)
            else:
                break         
    def finish(self):
        print("DEBUG: HandleClass() finished()")
        sock=self.request 
        x=sock.send(_b3)
        print("sended=",x)
    

class Server(TCPServer):
    def __init__(self):
        TCPServer.__init__(self,("0.0.0.0",2000),HandleClass)
        self.timeout=0.1
        self.que=Queue() # temporaly!!!
        self.buffer=bytes(0)
    
    def put(self,new_bytes):
        #self.buffer = self.buffer + new_bytes
        self.buffer += new_bytes
    
    def getFrame(self):
        return self.buffer 
    
    def getFrame_backup(self):
        _bytes=self.buffer[:]
        s=_bytes.find(0x02);
        if s == -1 :            
            return None 
        e=_bytes.find(0x03);
        if e == -1 :             
            return None     
        #print("DEBUG:s,e=",s,e)
        if s < e:
            self.buffer= _bytes[e:]
            #print("DEBUG: _bytes[s:e]=",_bytes[s:)
            return _bytes[s:e+1] # safer        
        # something wrong !  end < start  so , 
        self.buffer = _bytes[s:] # delete until start
        return None                  

#server.server_close()
if __name__ =="__main__" :    
    server=Server()     
    print("Sever....")
    server.serve_forever(0.1)
    server.handle_request()
    pass

print("__pacakge__",__package__)
