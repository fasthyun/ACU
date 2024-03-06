# work for pyhton3.6 
# because of 
#    1. ordreddict 
#    2. 

""" 
design 철학  
===========
 * desiger-qt를 사용해서 기초 디자인을 했지만, 실제는 직접 코드를 작성하였다. 이유는... 
 * 화면표시부와 네트워크 데이타 처리부를 따로 분리하고 
   그렇게 분리하는게 낫겠다 싶었는데 잘 안되었다.
 * qlayout이나 qlabel을 사용하지 않은 이유는 여러가지 제한 사항이 발생해서 그렇다.
   예를 들어 qt stylesheet는 기능은 많지만 내가 필요로하는 속성의 제한, 직접  애니메이션  넣기 제한 등등  
 * 표시부 widget는 용도에따라 코드재사용을 할수있게 설계하였다.   
 * Network처리부:
     스트림데이타가 조각나서 오는경우에 대해 손실없이 처리하는것에 대해 몇년동안 고민해 왔는데 
     이번 코드는  0x02, 0x03 시작 끝 Sync가 존재하는데 불구하고 이해하기 쉬우면서 꽤나 세련되게 
     작성되었다. 앞으로도 네트워크프로그램 작성할때 계속 사용할것 같다. 진작..이런 방법으로 했으면 ㅋ 
 
"""
ver=0.90
from PyQt5.QtWidgets import QApplication,QMainWindow, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QPainter, QImage, QPen, QColor
from PyQt5.QtCore import QTimer,QRect , Qt
from PyQt5 import uic

#from PyQt5 import rc
import weather_rc
import time
import datetime

from socket_server import Server, parse_KWEATHER

#form_ui, widget_class = uic.loadUiType('lcd_weather.ui')
server=None
# Screen init 
class MainWindow(widget_class,form_ui) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

class ItemWidget(QWidget) :
    def __init__(self, parent,_title) :
        super().__init__(parent)
        #print("parent= ", parent)
        self.drawBackground=False
        self.title1=_title
        self.color={"title_background":QColor(0,100,200) ,"value": None}
        self.config={"title":"title","pos":(0,0)}
        self.move(0,0)      
        self.value="-" # string is better???
    
    def setValue(self,val):
        self.value=val
        #draw 
        
    def changeSize(self,d=None):
        pw=self.parentWidget().width()
        ph=self.parentWidget().height()  - self.parentWidget().height()/10        
        
        #print("w=",w," , h=",h)
        #self.setBaseSize(w/3,h/3)
        #_height=self.height() 
        #_width=self.width()
        #_wd=pw/100
        #_hd=ph/50
        
        #self.resize(pw/3 -_wd*2 ,ph/3 -_hd*2 )  
        #_f=self.font()
        #_f.setPixelSize(_height/3 - _)
        #self.setFont(_f)
        
    def showEvent(self,event):
        ##print("show parent = " ,self.parentWidget())
        #w=self.parentWidget().width()
        #h=self.parentWidget().height()
        #self.setBaseSize(w/3,h/3)
        pass
    
    def drawTitle(self, p ): # painter
        _height=self.height()        
        _width=self.width()
        
        font = p.font();
        font.setPixelSize(_height/8);        
        p.setFont(font);
        
        d=_height/10        
        p.setBrush(self.color['title_background'])
        p.setPen(QPen(QColor(10, 10, 10), 1))        
        p.drawRect(0,0,_width ,_height/4  )
        r=QRect(10,0,_width - 10,_height/4)
        #br=QRect(2,2,_width-2,_height/4 - )
        p.setPen(QPen(QColor(255, 255, 255), 1))
        p.drawText(r,Qt.AlignVCenter | Qt.AlignLeft,self.title1)
        
    def paintEvent(self, event):
        #self.changeSize()
        _height=self.height()        
        _width=self.width()        
        d=_height/40        
        #print("w=",w," , h=",h)
        p = QPainter()
        p.begin(self)        
        #qp.drawImage(self.rect(),self.image_bg,self.image_bg.rect())
        #p.draw#Rect(self) 
        if self.drawBackground :
            p.setBrush(QColor(255, 255, 255))
            p.setPen(QPen(QColor(100, 100, 100), 3))
            p.drawRect(self.rect())            
            self.drawTitle(p)        
            
        font = p.font();
        font.setFamily("Gulim")
        font.setPixelSize(_height/2.3);         
        p.setFont(font);
        
        y1=_height*1/4
        #y1=_height*1/4
        r=QRect(0,y1,_width,_height*3/4) 
        p.setPen(QPen(QColor(1, 1, 1), 10))
        p.drawText(r, Qt.AlignVCenter | Qt.AlignHCenter ,str(self.value))        
        
        p.end()

class dateWidget(ItemWidget):
    def __init__(self, parent,_title) :
        super().__init__(parent,_title)
        self.value=""
        pass
        
    def setValue(self,_val):
        if type(_val) == datetime.datetime :            
            self.value= _val.strftime("%Y.%m.%d(%a) %H:%M")
        print("dateTime val =",type(self.value),_val)
    
    def moveEvent(self, e):
        print("dateWidget.moveEvent=",e.pos())       
            
    def resizeEvent(self, e):
        print("dateWidget.resizeEvent=",e.size())       
        p=self.parent()
       
    def paintEvent(self, event):        
        _height=self.height()
        _width=self.width()
        p = QPainter()
        p.begin(self)         
        
        #p.setBrush(QColor(210, 210, 210))        
        #p.drawRect(0,0,_width ,_height/2 )        
        font = p.font();
        font.setFamily("Sans")
        font.setPixelSize(_height);  
        p.setFont(font)
        #r=QRect(0,y1,_width,_height*) 
        p.setPen(QPen(QColor(10, 10, 10), 1))
        #self.value="aaaaaabafdsfasda"
        #print("rect=",self.rect())
        p.drawText(self.rect(), Qt.AlignVCenter | Qt.AlignRight ,str(self.value)) 
        #print("self.value=",self.value)
        p.end()
  
class WindDirectionWidget(ItemWidget):
    def __init__(self, parent,_title) :
        super().__init__(parent,_title)
        pass
    
    def setValue(self,_val):        
        val=_val 
        _val=float(_val)
        if 350 < _val < 360 and  0< _val <20 : 
            val="북"
        if 20< _val <70 : 
            val="북동"
        if 70< _val <110 : 
            val="동"        
        if 110< _val <160 : 
            val="남동"
        if 160< _val <200 : 
            val="남"
        if 200< _val <250 : 
            val="남서"            
        if 250< _val <290 : 
            val="서"
        if 290< _val <350 : 
            val="북서"      
        self.value=val
        #dra
    def paintEvent(self, event):
        super().paintEvent(event)
        """
        _height=self.height()        
        _width=self.width()        
        d=_height/40        
        #print("w=",w," , h=",h)
        p = QPainter()
        p.begin(self)               
        p.end()
        """
        pass
    
class MyWindow(QMainWindow):         
    def __init__(self):
        super().__init__()        
        self.setWindowTitle("Weather")
        self.setGeometry(100,100, 400, 300)
        self.setStyleSheet(" ")        
        #self.image_bg=QImage(":/image/sky_blue2.jpeg"); # a background image
        self.image_bg=QImage("./fake_background.png"); # a background image        
        self.widgets=[]
        self.dateWidget=None
        print("dateWidget=",self.dateWidget)
        for k in items.keys():
            it=items[k]
            #_obj=ItemWidget(self,_it['title'])
            _obj=it['class'](self,it['title']) # ItemWidget(self,"날씨")
            it["object"]=_obj
            if  k == "datetime" :
                self.dateWidget=_obj
            else:
                self.widgets.append(_obj)
            if "title_background" in it: #if it.hasKey() :
                    _obj.color["title_background"]=it["title_background"];
        self.showFullScreen()
        #self.setWindowState(self.windowState() ^ Qt.WindowFullScreen); 

    def showEvent(self,event):
        pass
            
    def mousePressEvent(self,e):
        self.setWindowState(self.windowState() ^ Qt.WindowFullScreen); 
        pass
        
    def resizeEvent(self, e):
        print("Mywindow.resizeEvent=",e.size())
        #size = e.size() # hmmm different...
        d=self.width()/100;
        _w=self.width() 
        _h=self.height() 
        
        _datetimeWidget_height=_h/15    
        
        _h -= _datetimeWidget_height + d*4
        _w -= d*4 # gap 
        x=d;
        y=d;
        for w in self.widgets:            
            w.move(x,y)
            w.resize(_w/3 , _h/3 )  
            tw=w.width()
            th=w.height()
            x= x + tw + d            
            if x > _w: 
                x = d;
                y = y+ th +d 
            w.changeSize(d)
        
        self.dateWidget.move(0,y)
        self.dateWidget.resize(self.width() - 2*d ,_datetimeWidget_height-d)
            
        
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)      
        qp.drawImage(self.rect(),self.image_bg,self.image_bg.rect())
        qp.end()
        
def onAppQuit():
    if server is not None:
        server.server_close()
        print("close server!!")
    #if app is not None:
    #    app.closeAllWindows()    
    
#orderedDictionary
items = {  
   "wind_direction" : { "title" :"풍향", "object": None ,"class":WindDirectionWidget },
   "wind_speed":{ "title" :"풍속(㎧)", "object": None ,"class": ItemWidget },
   "humidity": { "title" :"습도(％)", "object":  None ,"class":ItemWidget },
   "temp_now": { "title" :"현재온도(℃)", "object":  None ,"class": ItemWidget ,"title_background": QColor(0,180,10)}, # green
   "temp_high_day":{  "title" :"일최고기온(℃)", "object": None ,"class": ItemWidget, "title_background": QColor(180,10,10) },  # red 
   "temp_low_day": { "title" :"일최저기온(℃)", "object":  None ,"class": ItemWidget, "title_background": QColor(0,200,195) },  # cyan 
   "rainfall": { "title" :"강수량(㎜)", "object":  None ,"class": ItemWidget },
   "rainfall_yesterday": { "title" :"전일강수량(㎜)", "object": None ,"class": ItemWidget },
   "snowfall": { "title" :"적설량(㎝)", "object": None ,"class": ItemWidget },
   "datetime": { "title" :"", "object": None ,"class": dateWidget }
 }

server=Server()
app = QApplication([])
#widget = uic.loadUi('lcd_weather.ui')
app.aboutToQuit.connect(onAppQuit)

def timeout():
    #print("DEBUG: timeout()!",datetime.datetime.now())
    if server is not None:
        server.handle_request() # process the quequed network data 
        while server.que.qsize() !=0 : 
            _frame=server.que.get() 
            try :
                _dict=parse_KWEATHER(_frame)
                #print("received data _len= ",len(_data),_dict)
                for k in items.keys():
                    if k in _dict:
                        _val=_dict[k]
                        _it =items[k]
                        _it['object'].setValue(_val)
                        _it['object'].update()
            except Exception() as e :
                print(e)
        
    #time.sleep(0.1)
    pass

timer = QTimer()
timer.start(500)
timer.timeout.connect(timeout)

#window = widget #MainWindow()
window = MyWindow()
window.show()

app.exec()

del app
del server
