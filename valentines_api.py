import requests,sys,math,re
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.apiGET()
        self.screenSize=[QDesktopWidget().screenGeometry().width(),QDesktopWidget().screenGeometry().height()]
        self.resize(*self.screenSize)
        self.setWindowFlags( Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.label = QLabel() #add layout to center the label
        canvas = QPixmap(*self.screenSize) 
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        self.draw_something()
    

    def draw_something(self):
        padx=int(self.screenSize[0]/2)
        pady=int(self.screenSize[1]/2)
        painter = QPainter(self.label.pixmap())
        pen=QPen()

        #draw bg rect
        pen.setColor(self.colorPalette[0])
        pen.setWidth(10)
        painter.setPen(pen)
        brush = QBrush()
        brush.setColor(self.colorPalette[1])
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)
        #painter.drawRect(400,400,1900,1100)
        painter.drawRect(310,100+50,1300,900-20)

        #draw bg pattern
        pen.setWidth(0)
        painter.setPen(pen)
        brush = QBrush()
        brush.setColor(self.colorPalette[3])
        brush.setStyle(Qt.Dense7Pattern)
        painter.setBrush(brush)
        #painter.drawRect(400,400,1900,1100)
        painter.drawRect(310+5,100+50+5,1300-10,900-20-10)

        #draws heart
        pen.setWidth(4)
        pen.setColor(self.colorPalette[2])
        painter.setPen(pen)
        
        def xt(t):
            return (15 * math.sin(t) ** 3)
        def yt(t):
            return (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) *-1
        for i in range(5000):
            painter.drawLine(padx, pady,int(xt(i) * 20 + padx), int(yt(i) * 20 +pady))

        #draws text
        font=QFont()
        font.setPointSize(30 if self.lineLength>15 else 35)
        font.setFamily("Bahnschrift")
        pen.setColor(self.colorPalette[4])
        painter.setPen(pen)
        painter.setFont(font)
        #painter.drawText(0, pady-450, self.screenSize[0], self.screenSize[1], Qt.AlignHCenter, self.firstSentence)
        painter.drawText(0, pady-350, self.screenSize[0], self.screenSize[1], Qt.AlignHCenter, self.firstSentence)
        painter.drawText(0, pady+350, self.screenSize[0], self.screenSize[1], Qt.AlignHCenter, self.secSentence)

        painter.end()

        
    def apiGET(self):
        #pickup line
        obtainPickup = requests.get("https://vinuxd.vercel.app/api/pickup").json()["pickup"]
        obtainPickup=obtainPickup.split()
        self.lineLength=len(obtainPickup)
        half,rem=divmod(len(obtainPickup),2)
        self.firstSentence,self.secSentence=obtainPickup[:half+rem],obtainPickup[half+rem:]
        self.firstSentence="".join(i + " " for i in self.firstSentence)
        self.secSentence="".join(i + " " for i in self.secSentence)

        #palettes
        url = "https://zylalabs.com/api/211/color+palette+api/221/get+random+palette"
        payload = "{\r\n\"input\":[[255,192,203],\"N\",\"N\",\"N\"],\r\n\"model\":\"default\"\r\n}" 
        payload={}
        headers = {
            'Authorization': 'Bearer 826|YfgUkrWPh2hBNK9GVagdsQHbREnRWylsoZj69L3D'
        }
        color_request = requests.request("GET", url, headers=headers, data=payload).json()["result"]
        #color_request=[[21, 99, 116], [12, 125, 139], [254, 247, 209], [176, 201, 168], [111, 47, 61]]
        self.colorPalette=list(QColor(*i) for i in color_request)



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
