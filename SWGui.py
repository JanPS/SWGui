# -*- coding: utf-8 -*-

# SWGui - Einfache GUI-Programmierung
# Opensource
# Autoren R. Oldenburg, M. Rabel, J. Schuster, Uni Frankfurt 
# Kontakt oldenbur@math.uni-frankfurt.de

# QT-Version von SWGui

# Version 2.2 mit Inter-Thread-Kommunikation vom 24.01.2013

# Import & Init .........................................................



# to button mit Bildern
# tabelle ohne header

from PyQt4 import QtGui
from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import QtWebKit

try:
  import MySQLdb
except:
  pass


import math
import sys,os
import inspect
def nargs(someMethod): 
    """nargs(f) returns the number or arguments f takes
    
    """
    return len(inspect.getargspec(someMethod).args)

TheCursor=None

def SWclose(): 
    """Schließt das SWGui Fenster

    Die QT-Infrastruktur bleibt erhalten."""
    print "Entering swclose"
    try: TheMainWin.close()
    except: print "TheWin not closed"
    try: QtCore.pyqtRemoveInputHook()
    except: print "Hook not removed"
    try: 
        TheApp.exit()
        del TheApp
    except: print "The App not destroyed"

def SWstart(): 
    """Startet die Ereignisbehhandlung von QT

    SWstart braucht in der Regel NICHT aufgerufen zu werden. 
    unter IDLE ist es nötig."""
    global SWisRunning
    SWisRunning=True
    TheMainWin.show()
    t=TheApp.exec_()
    SWisRunning=False
    return t

def SWinteract():
    """Ermöglicht die Ereignisbehhandlung von QT

    SWinteract benötigt man in Programmen, die eine eigene Endlosschleife implementieren, 
    so dass die QT-Ereignisse nicht verarbeitet werden können. 
    Gelegentlich Aufruf von SWinteract erlaubt dann die Event-Behandlung und aktualisiert
    das Fesnter."""
    TheMainWin.update()
    TheApp.processEvents()
    TheMainWin.updateGeometry()


def SWclear():
    """Löscht alle Elemente des Hauptfensters

    Nach SWclear können neue Widgets erzeugt werden."""
    global TheWin,TheCursor,TheMainContainer
    TheWin=QtGui.QWidget()
    TheMainWin.setCentralWidget(TheWin)
    TheWin.TheLayout=QtGui.QVBoxLayout()
    TheMainContainer=TheWin.TheLayout
    TheWin.setLayout(TheWin.TheLayout)
    TheWin.show()
    TheCursor=TheWin.TheLayout

SWKeyTable={
    QtCore.Qt.Key_Left:"left",
    QtCore.Qt.Key_Right:"right",
    QtCore.Qt.Key_Up:"up",
    QtCore.Qt.Key_Down:"down",
    QtCore.Qt.Key_Tab:"tab",
    QtCore.Qt.Key_Return:"return"
    }




def SWdoCmd(cmd):
    SWDo(TheWin,"doCmd", Qt.QueuedConnection, QtCore.Q_ARG(type(cmd),cmd) );

def SWdo(objekt, methode, *args):
    apply(QtCore.QMetaObject.invokeMethod,[objekt, methode,QtCore.Qt.QueuedConnection]+
          map(lambda x: QtCore.Q_ARG(type(x),x) ,list(args)))
          

class SWWidget(QtGui.QWidget):
    def __init__(self): 
        QtGui.QWidget.__init__(self)
        self.commands={}
        self.anyKeyCommand=None
    def doCmd(self,cmd): return eval(cmd)
    def keyPressEvent(self,event):
        if SWKeyTable.has_key(event.key()):  
            te=SWKeyTable[event.key()]
        else: te=str(event.text())
        if self.commands.has_key(te):
            if self.commands[te]!=None:
                return self.commands[te]()
        else:
            if self.anyKeyCommand==None: return
            self.anyKeyCommand(te)
    def setKeyCommand(self,key,cmd): self.commands[key]=cmd

def setKeyCommand(key,cmd):
    """setKeyCommand(key, cmd) -  Befehhl cmd, wenn Taste key
    
    cmd ist eine parameterlose Funktion. key ist ein String, zB
    'a' oder 'A' oder 'CTRL-Z' oder 'return'
    Beispiel: setKeyCommand('x', cmd) """ 
    global TheWin
    if type(key)==str:
        if key.startswith("CTRL-") and len(key)>=6:
            key=chr(ord(key[5].upper())-64)
            print "Key set", key
    TheWin.setKeyCommand(key,cmd)

def setAnyKeyCommand(cmd): 
    """setAnyKeyCommand(kcmd) -  Befehhl cmd, wenn beliebige Taste
    
    cmd ist eine parameterlose Funktion""" 
    global TheWin
    TheWin.anyKeyCommand=cmd
    

SWisRunning=False


def SWinit():
    global TheApp,TheMainWin,TheWin,TheCursor,TheMainContainer
    TheApp = QtGui.QApplication([])
    TheApp.setQuitOnLastWindowClosed(True)
    TheMainWin=QtGui.QMainWindow()
    #TheWin=QtGui.QWidget()
    TheWin=SWWidget()
    TheMainWin.setCentralWidget(TheWin)
    TheWin.TheLayout=QtGui.QVBoxLayout()
    TheWin.setLayout(TheWin.TheLayout)
    TheMainContainer=TheWin.TheLayout
    #TheWin.show()
    TheCursor=TheWin.TheLayout
    TheMainWin.connect(TheWin, QtCore.SIGNAL("closed()"),SWclose)
    TheMainWin.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
    TheWin.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)




def SWshow(*args):
    """SWshow() zeigt das SWGui-Fenster an
    
    """
    args=list(args)
    if args==[]: TheMainWin.show()
    else: 
        if args[0]==True: TheMainWin.show()
        else: TheMainWin.hide()


try: 
    TheMainWin0=TheMainWin # Wenn das keinen Fehler auslöst, dann Warmstart
    del TheApp
except: 
    SWinit()

SWCursorStack=[TheCursor]

def SWLastContainer():
    """SWLastContainer() wechselt den aktuellen Container zum vorhergehenden
    
    Neue Widgets werden dann in den davor aktuellen Container gesetzt"""
    global TheCursor,SWCursorStack
    if len(SWCursorStack)>1:
        TheCursor=SWCursorStack[1]
        SWCursorStack=SWCursorStack[1:]

def SWsetWindowTitle(s): 
    """SWsetWindowTitle(s) setzt den Titel des Fensters
      
    """
    assert isinstance(s,str) or isinstance(s,unicode) 
    TheMainWin.setWindowTitle(s)

def SWsetWindowIcon(i): 
    """SWsetWindowIcon(i) setzt das Icon des fensters
      
    i kann sein ein Dateiname einer Bilddatei oder ein QT-Pixelbild"""
    TheMainWin.setWindowIcon(QtGui.QIcon(i))

def SWsetWidgetSize(widget,breite,hoehe):
    """SWsetWidgetSize(widget,breite,hoehe) setzt die Groesse eines Widgets
      
    """
    assert isinstance(breite,int)
    assert isinstance(hoehe,int)
    assert breite>=0
    assert hoehe>=0
    rect=widget.geometry()
    widget.setGeometry(rect.x(),rect.y(),breite,hoehe)

def SWsetWindowSize(breite,hoehe): 
    """SWsetWindowSize(breite,hoehe) setzt die Groesse des Fensters
      
    """
    assert isinstance(breite,int)
    assert isinstance(hoehe,int)
    assert breite>=0
    assert hoehe>=0
    rect=TheMainWin.geometry()
    TheMainWin.setGeometry(rect.x(),rect.y(),breite,hoehe)


# Tools fuer Farben ................................................
SWColMap={"red": [255,0,0], "green": [0,255,0], "blue": [0,0,255],
          "black": [0,0,0], "white": [255,255,255], "gray": [128,128,128],
          "yellow": [255,255,0], "magenta": [255,0,255], "cyan":[0,255,255] }  
          
def mkQCol(col): 
    """mkCol(col) erzeugt eine Farbe aus verschiedenen Angaben
    
    col kann sein eine Zeichenkette "black", "red",...., eine RGB-Liste [255,0,255],
    oder eine 32-Bit-Zahl"""
    if col==None: return col
    if type(col)==QtGui.QColor: return col
    if type(col)==long: return QtGui.QColor(col)
    if type(col)==str:
        if col in SWColMap.keys(): col=SWColMap[col]
        else: raise Exception("Unkonwn Color string: "+col)
    if type(col)==int or type(col)==float: col=[col,col,col]
    col=map(int,col)
    if len(col)==3: return apply(QtGui.QColor.fromRgb,col)
    if len(col)==4: return apply(QtGui.QColor.fromRgba,col)
    raise(TypeError("No Color: "+str(col)))
def mkQColNum(col): 
    if type(col)==int and col>1000: return col
    else: return mkQCol(col).rgba()
  

# Widget Klassen .....................................................
class SWVBox(QtGui.QVBoxLayout):
    """SWVBox ist ein Contaner, der Widgets vertikal anordnet
    
    SWVBox() erzeugt eine Box an der aktuellen Cursorposition
    SWVBox(c)erzeugt eine Box innerhalb eines anderen Containers"""
    def __init__(self,container=None):
        global TheCursor,SWCursorStack
        QtGui.QVBoxLayout.__init__(self)
        if container==None: self.layout = TheCursor
        else: self.layout =container
        self.layout.addLayout(self)
        TheCursor=self
        SWCursorStack=[self]+SWCursorStack

class SWHBox(QtGui.QHBoxLayout):
    """SWHBox ist ein Contaner, der Widgets vertikal anordnet
    
    SWHBox() erzeugt eine Box an der aktuellen Cursorposition
    SWHBox(c)erzeugt eine Box innerhalb eines anderen Containers"""
    def __init__(self,container=None):
        global TheCursor,SWCursorStack
        QtGui.QHBoxLayout.__init__(self)
        if container==None: self.layout = TheCursor
        else: self.layout =container
        self.layout.addLayout(self)
        TheCursor=self
        SWCursorStack=[self]+SWCursorStack


class SWButton(QtGui.QPushButton): # Text setzen mit setText
    """SWButton : Button-Klasse
    
    SWButton(container=None,text='', command=None)
    command ist eine Funktion mit einem oder keinem Argument,
    die aufgerufen wird, wenn der Button gedrueckt wird.
    Es wird der Button selbst als Argument uebergeben.
    """
    def __init__(self, text='', container=None, command=None, **options):
        assert isinstance(text,str) or isinstance(text,unicode)
        QtGui.QPushButton.__init__(self,text)
        self.setCommand(command)
        if container==None: self.layout = TheCursor
        else: self.layout =container
        self.layout.addWidget(self)
        self.command=command
        self.clicked.connect(self.cmd)
    def cmd(self,ignored): 
        if self.command!=None:
            if nargs(self.command)==0: return self.command()
            elif nargs(self.command)==1: return self.command(self)
            else: raise Exception("SWButton click command called with wrong number of arguments")
    def setCommand(self,cmd):
        """Setzt die Aktion, die ein Button bewirkt

        cmd wird bei Klick auf den Buton aufgerufen (1 Argumentm der Button selbst),
        oder kein Argument."""
        self.command=cmd
        #if cmd!=None: self.clicked.connect(cmd)
    def setSize(self,w,h):
        """setSize(w,h) setzt breite und hoehe des Widgets
        
        """
        assert isinstance(w,int)
        assert isinstance(h,int)
        return self.resize(w,h) # setValue  ererbet
    def getText(self):
        """getText() liefert den Text auf einem Button
        
        
        """
        return str(self.text())

class SWCheckBox(QtGui.QCheckBox): # isChecked() to query; setChecked(bool)  
    def __init__(self, text="",container=None, command=None, **options):
        QtGui.QCheckBox.__init__(self,text)
        self.command=command
        self.stateChanged.connect(self.cmd)
        if container==None: self.layout = TheCursor
        else: self.layout =container
        self.layout.addWidget(self)
    def cmd(self,*arg): 
        if self.command!=None:
            if nargs(self.command)==0:
                self.command()
            else:
                if nargs(self.command)==1:
                    self.command(self.isChecked())
                else:
                    if nargs(self.command)==2:
                        self.command(self.isChecked(),self)
                    else: raise Exception("SWCheckBox called with too many args.") 
    def setText(self,s):
        """Setzt den Text einer Checkbox

        s kann ein beliebiger String sein"""
        assert isinstance(s,str) or isinstance(s,unicode)
        self.setText(s)
    def setCommand(self,s): 
        """Setzt die Aktion, die eine Checkbox bewirkt

        cmd bekommt zwei Argumente (checked?,Checkbox), eines (checked?),
        oder keins."""
        self.command=s


class SWSlider(QtGui.QSlider):
    def __init__(self, orient, min, start,max,container=None, command=None):
        if orient in ["h","H","Horizontal","horizontal"]: 
            QtGui.QSlider.__init__(self,0x1)
            self.dir="h"
        else: 
            QtGui.QSlider.__init__(self,0x2)
            self.dir="v"
        self.setRange(min,max)
        self.setValue(start)
        self.setTickPosition(2)
        self.command=command
        self.valueChanged.connect(self.cmd)
        if container==None: self.layout = TheCursor
        else: self.layout =container
        self.layout.addWidget(self)
    def cmd(self,*arg): 
        if self.command!=None:
            if nargs(self.command)==0:
                self.command()
            else:
                if nargs(self.command)==1:
                    self.command(self.value())
                else:
                    if nargs(self.command)==2:
                        self.command(self.value(),self)
                    else: raise Exception("SWSlider called with too many args.") 
    def setCommand(self,s): 
        """Setzt die Aktion, die beim Schieben des Sliders ausfgerufen wird

        cmd bekommt zwei Argumente (wert,slider) oder eines (wert),
        oder kein Argument haben."""
        self.command=s
    def getValue(self):  # Parallel dazu setValue
        """getValue() liefert den Wert eines Sliders
        
        """
        return self.value() # setValue  ererbet
    def setSize(self,w,h):
        """setSize(w,h) setzt breite und hoehe des Widgets
        
        """
        return self.resize(w,h) # setValue  ererbet

class SWTextField(QtGui.QLineEdit):
    """SWTextField Ein/Ausgabezeile fuer Text
    
    """
    # Ererbt: setMaxLength(c)
    def __init__(self, container=None,text='', command=None,**options):
        QtGui.QLineEdit.__init__(self,text)
        self.setCommand(command)
        if container==None: self.layout = TheCursor
        else: self.layout =container
        self.layout.addWidget(self)
        self.command=command
        self.returnPressed.connect(self.cmd)
        self.changeCommand=None
        self.textChanged.connect(self.chgcmd)
        self.keyEvent=None
        self.keyEventC=None
    def event(self, event):
            if event.type()==QtCore.QEvent.KeyPress:
                if self.keyEvent!=None:
                    self.keyEvent(event.key())
                if self.keyEventC!=None:
                    self.keyEventC(event.text())
            return QtGui.QLineEdit.event(self, event)
    def cmd(self):
        if self.command!=None:
            if nargs(self.command)==0: self.command()
            else:
                if nargs(self.command)==1: self.command(self)
                else: raise Exception("SWTextField event handler with too many args.")
    def setCommand(self,cmd):
        """Setzt die Aktion bei Enter-Taste im TextField

        cmd wird bei Enter im TextField aufgerufen (1 Argument, das TextField selbst),
        oder kein Argument."""
        self.command=cmd
        #if cmd!=None: self.clicked.connect(cmd)
    def chgcmd(self):
        if self.changeCommand!=None:
            if nargs(self.changeCommand)==0: self.changeCommand()
            else:
                if nargs(self.changeCommand)==1: self.changeCommand(self.getText())
                else: raise Exception("SWTextField event handler with too many args.")
    def setChangeCommand(self,cmd):
        """Setzt die Aktion bei jeder Textänderung aufgerufen wird
        
        cmd bekommt ein Argument, den neuen Text """
        self.changeCommand=cmd
    def setKeyCommand(self,cmd):
        """Setzt die Aktion bei Tastendruck
        
        cmd bekommt ein Argument, die Tastennummer"""
        self.keyEvent=cmd
    def setKeyCCommand(self,cmd):
        """Setzt die Aktion bei Tastendruck
        
        cmd bekommt ein Argument, die Taste als str """
        self.keyEventC=cmd
    def setBackgroundColor(self,col):
        if isinstance(col,QtGui.QColor): col=col.name()
        if isinstance(col,str): 
            self.setStyleSheet('QLineEdit { background-color: '+col+'; }')
    def getText(self): return str(self.text()) # setText  ererbt
    def getFloat(self):
        try:
            return float(str(self.text()))
        except: return float("nan")
    def getInt(self):
        try:
            return int(str(self.text()))
        except: return float("nan")
    def getEval(self):
        try:
            return eval(str(self.text()))
        except: return None


class SWTextEdit(QtGui.QTextEdit):
    """SWTextEdit Ein/Ausgabe fuer Text
    
    """
    # Ererbt: setMaxLength(c)
    def __init__(self, container=None,text='', command=None,**options):
        QtGui.QTextEdit.__init__(self,text)
        self.setCommand(command)
        if container==None: self.layout = TheCursor
        else: self.layout =container
        self.layout.addWidget(self)
        self.command=command
        self.textChanged.connect(self.cmd)
    def cmd(self):
        if self.command!=None:
            try: self.command(self)
            except TypeError:
                self.command()
    def setCommand(self,cmd):
        """Setzt die Aktion bei Enter-Taste im TextEdit

        cmd wird bei Enter im TextEdit aufgerufen (1 Argument, das TextField selbst),
        oder kein Argument."""
        self.command=cmd
        #if cmd!=None: self.clicked.connect(cmd)
    def getText(self): return str(self.toPlainText()) # setText  ererbt



class SWHTMLDisplay(QtWebKit.QWebView):
    """SWHTMLDisplay zeigt HTML an
    
    """
    # Ererbt: setMaxLength(c)
    def __init__(self, container=None,text='', command=None):
        QtWebKit.QWebView.__init__(self)
        if container==None: self.layout = TheCursor
        else: self.layout =container
        self.layout.addWidget(self)
        self.setText(text)
        self.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.linkClicked.connect(lambda b: self.cmd(b))
        self.command=command
    def setText(self,text): 
        assert isinstance(text,str) or isinstance(text,unicode)
        self.setHtml(text)
    def getText(self): return str(self.toPlainText()) # setText  ererbt
    def setCommand(self,cmd):
        """Setzt die Aktion bei Klick auf einen Link 

        cmd wird bei Klick auf Link aufgerufen (2 Argument: self und  Link),
        oeder ein Argument (Link) oder kein Argument."""
        self.command=cmd
    def cmd(self,*arg):
        try: url=str(arg[0].toString())
        except: url=unicode(arg[0].toString())
        url=unicode(arg[0].toString())
        #print "cmd", url
        if self.command!=None:
            try: self.command(self,url)
            except TypeError:
                try: self.command(url)
                except TypeError:
                    try: self.command()
                    except: pass                





class SWLabel(QtGui.QLabel):
    def __init__(self, text="",container=None, **options):
        QtGui.QLabel.__init__(self,text)
        if container==None: self.layout = TheCursor
        else: self.layout =container
        self.layout.addWidget(self)
    def setOrientation(self,dir): #??????
        if dir.upper()=="L": self.setAlignment(QtCore.Alignment(0));
        if dir.upper()=="R": self.setAlignment(QtCore.Alignment(1));
        if dir.upper()=="C": self.setAlignment(QtCore.Alignment(2));
    def getText(self):
        """getText() liefert den Text auf einem Button
        
        
        """
        return str(self.text())


class SWComboBox(QtGui.QComboBox):
    def __init__(self, ItemList=[],command=None, container=None, **options):
        QtGui.QComboBox.__init__(self)
        if container==None: self.layout = TheCursor
        else: self.layout =container
        self.layout.addWidget(self)
        self.itemList=[]
        for x in ItemList: self.addItem(x)
        self.currentIndexChanged.connect(lambda i: self.cmd(i))
        self.command=command  
    def setCommand(self,cmd):
        """Setzt die Aktion bei Wahl eines neuen Items aus der ComboBox 

        cmd wird mit 3 Argumenten aufgerufen: Die Box, der Index und das Item,
        oder mit 2 Argumenten: Box, Item, 
        oder mit einem Argument: Item
        oder ohne Argumente"""
        self.command=cmd
    def cmd(self,i):
        if self.command!=None: 
            self.command(self,self.currentText())
    def addItem(self,text):
        if text in self.itemList: return
        self.itemList.append(text)
        QtGui.QComboBox.addItem(self,text)
        
# Direkt von QCombonBox geerbt und nützlich
# currentText(), currentIndex(), addItem(text), removeItem(index)
# insertitem(index,text), count(),...    
        


class SWList(QtGui.QListWidget):   
    # addItem interessant
    def __init__(self, zeilen=0,container=None, command=None, **options):
        QtGui.QListWidget.__init__(self)
        for i in range(zeilen): self.addItem("")
        if container==None: self.layout = TheCursor
        else: self.layout =container
        self.layout.addWidget(self)
        self.setChangedCommand(command)
        self.setClickCommand(command)
        self.itemClicked.connect(self.clickCMD)
        self.itemChanged.connect(self.changeCMD)
    def setChangedCommand(self,s): # Kommando bekommt table, zeile
        """setChangedCommand setzt den Befehl, der beim Editieren aufgerufen wird
        
        Die übergebene Funktion nimmt entweder kein Argument oder zwei (sich selbst und Zeile)"""
        self.chCMD=s
    def setClickCommand(self,s): # Kommando bekommt table zeile 
        """setClickCommand setzt den Befehl, der beim KLicken aufgerufen wird
        
        Die übergebene Funktion nimmt entweder kein Argument oder zwei (sich selbst und Zeile)"""
        self.clCMD=s
    def changeCMD(self,qlwi):
        if self.chCMD!=None: 
            try: self.chCMD(self,self.ze(qlwi))
            except TypeError:
                self.chCMD()
    def clickCMD(self,qlwi):
        if self.clCMD!=None: 
           try: self.clCMD(self,self.ze(qlwi))
           except TypeError:
                self.clCMD()
    def ze(self,item): # Gibt Nummer des Items
        for i in range(self.count() ):
            if QtGui.QListWidget.item(self,i)==item: return i
        return -1
    def addItems(self,list): 
        for x in list: self.addItem(x)
    def setItem(self,z,text):
        assert isinstance(text,str) or isinstance(text,unicode)
        assert isinstance(z,int)
        if type(text)!=str and type(text)!=unicode: text=str(text)
        QtGui.QListWidget.setItem(self,z,QtGui.QListWidgetItem(text))
    def getItem(self,z): 
        assert isinstance(z,int)
        try: return str(self.item(z).data(0).toString())
        except: return ""
    def getItems(self):
        Z=self.count() 
        return [self.getItem(z) for z in range(Z)]


class SWTable(QtGui.QTableWidget):   
    def __init__(self, zeilen,spalten,container=None, command=None, **options):
        QtGui.QTableWidget.__init__(self,zeilen,spalten)
        if container==None: self.layout = TheCursor
        else: self.layout =container
        self.layout.addWidget(self)
        self.setChangedCommand(command)
        self.setRowHeaders(["Zeile "+str(i) for i in range(zeilen)])
        self.setColHeaders(["Spalte "+str(i) for i in range(spalten)])
        for z in range(zeilen):
            for s in range(spalten):
                QtGui.QTableWidget.setItem(self,z,s,QtGui.QTableWidgetItem(""))
        self.conn=None # DatabaseConnection
        self.name=None # Name der Tabelle in DB
    def newRow(self,zeile,titel=""):
        self.insertRow(zeile)
        self.setRowHeaders(self.RowHeaders[:zeile]+[titel]+self.RowHeaders[zeile:])
        for s in range(self.rowCount()):
            QtGui.QTableWidget.setItem(self,zeile,s,QtGui.QTableWidgetItem(""))
    def newCol(self,sp,titel=""):
        self.insertColumn(sp)
        self.setColHeaders(self.ColHeaders[:sp]+[titel]+self.ColHeaders[sp:])
        for z in range(self.columnCount()):
            QtGui.QTableWidget.setItem(self,z,sp,QtGui.QTableWidgetItem(""))
    def setChangedCommand(self,s): # Kommando bekommt zeile und spalte
        if s!=None:
            self.cellChanged.connect(lambda ze,sp: s(ze,sp))
    def setClickCommand(self,s): # Kommando bekommt zeile und spalte
        if s!=None:
            self.cellClicked.connect(lambda ze,sp: s(ze,sp))
    def setClickedCommand(self,s): # Kommando bekommt zeile und spalte
        if s!=None:
            self.cellClicked.connect(lambda ze,sp: s(ze,sp))
    # --------------- Beginn aenerungen
    def reactToActivate(self,cell):
        print "React to activate ",cell, self.itemHandler.has_key(cell)
        if self.itemHandler.has_key(cell):
            if self.itemHandler[cell]!=None: self.itemHandler[cell]()
    def setColHeaderClickCommand(self,cmd): # Setzt Eventhandler (1 args) für Klick auf Header
        self.horizontalHeader().sectionPressed.connect(cmd)
    def setRowHeaderClickCommand(self,cmd): # Setzt Eventhandler (1 args) für Klick auf Header
        self.verticalHeader().sectionPressed.connect(cmd)
    # Ende 
    def setItem(self,z,s,text):
        if type(text)!=str: text=str(text)
        assert isinstance(s,int)
        assert isinstance(z,int)
        QtGui.QTableWidget.setItem(self,z,s,QtGui.QTableWidgetItem(text))
    def getItem(self,z,s): 
        assert isinstance(s,int)
        assert isinstance(z,int)
        try: return str(self.item(z,s).data(0).toString())
        except: return ""
    def getItemsTransposed(self):
        Z=self.rowCount() 
        S=self.columnCount()
        return [[self.getItem(z,s) for z in range(Z)] for s in range(S)]
    def getItems(self):
        Z=self.rowCount() 
        S=self.columnCount()
        return [[self.getItem(z,s) for s in range(S)] for z in range(Z)]
    def getData(self):
        return [[self.getColHead(i) for i in range(self.columnCount())]]+self.getItems()
    def fillData(self,data):
        # data==[[H1,H2,...],[D11,D12,...],...]
        # if H1=='id' dont use this
        if data==None: return
        assert(type(data)==list)
        #print "Daten in fillDaTA", data
        n=len(data)-1
        if n==-1: return 
        m=len(data[0])
        self.setRowCount(n)
        self.setColumnCount(m)
        self.setColHeaders(data[0])
        for i in range(n):
            for j in range(m):
                QtGui.QTableWidget.setItem(self,i,j,QtGui.QTableWidgetItem(str(data[i+1][j])))
        if data[0][0]=='id':
            self.setColumnEditable(0,False)
        self.showVerticalHeader(False)    
    def setColHeaders(self,namelist):
        self.ColHeaders=namelist
        self.setHorizontalHeaderLabels(namelist)
    def setRowHeaders(self,namelist): 
        self.RowHeaders=namelist
        self.setVerticalHeaderLabels(namelist)
    def setColHead(self,i,text):
        self.horizontalHeaderItem(i).setText(text)
    def setRowHead(self,i,text):
        self.verticalHeaderItem(i).setText(text)
    def getColHead(self,i):
        return str(self.horizontalHeaderItem(i).text())
    def getRowHead(self,i):
        return str(self.verticalHeaderItem(i).text())
    def setCellEditable(self,z,s,yes):
        """setCellEditable(rowNumber,colNumber,yesno) set cell to be editable or not
        
        """
        if self.item(z,s)==None: return
        if yes:
            self.item(z,s).setFlags( QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled )
        else:
            self.item(z,s).setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
    def setRowEditable(self,z,yes):
        for i in range(self.columnCount()): self.setCellEditable(z,i,yes)
    def setColumnEditable(self,s,yes):
        for i in range(self.rowCount()): self.setCellEditable(i,s,yes)
    def setBackgroundColor(self, z,s, col):
        self.item(z,s).setBackgroundColor(mkQCol(col))
    def setTextColor(self, z,s, col):
        self.item(z,s).setTextColor(mkQCol(col))
    def setFontSize(self, *args):
        args=list(args)
        if len(args)==3: 
            [z,s,n]=args
            self.item(z,s).setFont(QtGui.QFont("Arial",pointSize=n))
        else: 
            if len(args)==1: 
                n=int(args[0])
                for z in range(self.rowCount()):
                    for s in range(self.columnCount()): 
                        self.item(z,s).setFont(QtGui.QFont("Arial",pointSize=n))
        self.update()
    def minimumSizeHint(self): 
        return QtCore.QSize(self.columnCount()*100+80, 50+self.rowCount()*20)
    def showHorizontalHeader(self,yesno):
        if yesno: self.horizontalHeader().show()
        else: self.horizontalHeader().hide()
    def showVerticalHeader(self,yesno):
        if yesno: self.verticalHeader().show()
        else: self.verticalHeader().hide()
    def connectDB(self,server,usr,pwd,dbname,tablename=None):
        """connectDB(server,usr,pwd,dbname) Connect to a database server
        
        Example: t.connectDB("dbserver.hosteurope.de","user02","dsf897z","datenbank1") 
        """
        self.conn=MySQLdb.connect(host=server,user=usr,passwd=pwd,db=dbname)
        self.name=tablename
    def closeDB(self):
        """closeDB() Close Connection to a database server
        
        """
        self.conn.close()
        self.conn=None
    def refresh(self):  
        if self.name!=None: return self.fillFromDBData(self.name)
        return False
    def fillFromDBData(self,tabellenname=None):
        """fillFromDBData yields the data of table tablename in connected database as list of lists
        
        returns true upon success"""
        if tabellenname==None: tabellenname=self.name
        d=getDBData(self.conn,tabellenname)
        if d==None: return False
        else:
            self.fillData(getDBData(self.conn,tabellenname))
            return True
    def writeToDB(self,tabellenname=None,overwrite=False,withAutoIndex=False):
        """writeToDB(tablename) write current table to database under given name
        
        """
        if tabellenname==None: tabellenname=self.name
        self.name=tabellenname
        return writeToDB(self.conn,tabellenname,self.getData(),overwrite,withAutoIndex)
    def getDBTables(self): return getTableNames(self.conn)
    def appendList(self,data):
        n=self.rowCount()
        self.newRow(n,titel="")
        for i in range(0,min(len(data),self.columnCount())):
            self.setItem(n,i,data[i])
        if self.name!=None and self.conn!=None: 
            try: insertListDB(self.conn,self.name,data)
            except: pass
    def fillFromSQLquery(self,query):
        self.fillData(SQLqueryDB(self.conn,query))
        self.name=None
        
        
#  ---------------- databasetools


DBTableList={} # Dctionary tablename -> columns for those tables that have auto index key

def dropTableFromDB(conn,tabellenname):
    """dropTableFromDB(conn,tablename) remove table from  database
    
    """
    assert(type(tabellenname)==str)
    cursor = conn.cursor()
    befehl="DROP TABLE "+tabellenname
    try: cursor.execute(befehl)
    except: pass

def createTableInDB(conn,tabellenname,spaltennamen,overwrite=False,withAutoIndex=False):
    """createTableInDB(conn,tablename,columns,owerwrite=False,withAutoIndex=False) creates a new table in database
    
    overwrites existing table if overwrite is True
    an automtaic primary key index is created when withAutoIndex=True
    colums is list of string (colums headers)
    returns True upon success"""
    if not(overwrite): 
        if tabellenname in getTableNames(conn):
            return False
    assert(type(tabellenname)==str)
    cursor = conn.cursor()
    befehl="DROP TABLE "+tabellenname
    try: 
        cursor.execute(befehl)
        #print "Tabelle geloescht mit Befehl ", befehl
    except: pass
    if withAutoIndex:
        befehl="CREATE TABLE "+tabellenname+" (`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY  "
        if spaltennamen[0]!="id":
            befehl=befehl+", "+spaltennamen[0]+" VARCHAR(45)"
        for spalte in spaltennamen[1:]:
            befehl += ", "+spalte+" VARCHAR(45)"
        befehl += ")"
        DBTableList[tabellenname]=spaltennamen
    else:
        befehl="CREATE TABLE "+tabellenname+" ("+spaltennamen[0]+" VARCHAR(45)"
        for spalte in spaltennamen[1:]:
            befehl += ", "+spalte+" VARCHAR(45)"
        befehl += ")"
        if DBTableList.has_key(tabellenname): DBTableList.pop(tabellenname)
    #print "SQL:",befehl
    try: cursor.execute(befehl)
    except: 
        print 'error creating table '
        cursor.close()
        return False
    conn.commit()
    cursor.close()
    return True

def insertListDB(conn,tablename,newrow):
    assert(type(tablename)==str)
    assert(type(newrow)==list)
    cursor = conn.cursor()
    if DBTableList.has_key(tablename):
        spalten=DBTableList.has_key[tablename]
        if len(spalten)!=len(newrow):
            raise Exception("insertListDB wrong number of attributes")
        befehl = "INSERT INTO  "+tablename+"  ("+spalten[0]
        for z in spalten[1:]: befehl=befehl+" ,"+z
        befehl=befehl+") VALUES ('"+str(newrow[0])+"'"
        for z in newrow[1:]:
            befehl += ", '"+str(z)+"'"
        befehl += ")"
    else:
        befehl = "INSERT INTO  "+tablename+" VALUES ('"+str(newrow[0])+"'"
        for z in newrow[1:]:
            befehl += ", '"+str(z)+"'"
        befehl += ")"
    cursor.execute(befehl)
    conn.commit()
    cursor.close()


def writeToDB(conn,tabellenname,daten,overwrite=False,withAutoIndex=False):
    """writeToDB(conn,tablename,data) write data to database under given name
    
    """
    if not(createTableInDB(conn,tabellenname,daten[0],overwrite,withAutoIndex)): return False
    #print "Tabelle angelegt"
    cursor=conn.cursor()
    for newrow in daten[1:]:
        if DBTableList.has_key(tabellenname):
            spalten=DBTableList[tabellenname]
            if len(spalten)!=len(newrow):
                raise Exception("insertListDB wrong number of attributes")
            befehl = "INSERT INTO  "+tabellenname+"  ("+spalten[0]
            for z in spalten[1:]: befehl=befehl+" ,"+z
            befehl=befehl+") VALUES ('"+str(newrow[0])+"'"
            for z in newrow[1:]:
                befehl += ", '"+str(z)+"'"
            befehl += ")"
        else:
            befehl = "INSERT INTO  "+tabellenname+" VALUES ('"+str(newrow[0])+"'"
            for z in newrow[1:]:
                befehl += ", '"+str(z)+"'"
            befehl += ")"
        #print befehl
        cursor.execute(befehl)
        conn.commit()
    cursor.close()
    return True

def getDBData0(conn,tabellenname,datennamen):
    """getDBData0(conn,tablename,colnames) fetches colums from the data table (list of lists) from a DB
    
    colnames ist list of strings of names of selected columns"""
    assert(type(tabellenname)==str)
    try:
        cursor = conn.cursor()
        namen=""
        for n in datennamen: namen=namen+n+", "
        namen=str(namen[:-2])
        tabellenname=str(tabellenname)
        cursor.execute("SELECT "+namen+" FROM "+tabellenname) 
        res=[datennamen]+map(list,cursor.fetchall()) 
        cursor.close()
        return res
    except: return None

def getDBData(conn,tabellenname):
    """getDBData(conn,tablename) fetches the data table (list of lists) from a DB
    
    """
    assert(type(tabellenname)==str)
    hds=getDBTableHeaders(conn,tabellenname)
    d=getDBData0(conn,tabellenname,hds)
    return d

def getDBTableHeaders(conn,tabellenname): 
    """getDBTableHeaders(conn,tabblename) Get headers (attributes) in table
    
    """
    assert(type(tabellenname)==str)
    try:
        cursor = conn.cursor()
        befehl=str("SHOW COLUMNS FROM "+tabellenname)
        cursor.execute(befehl)
        s=cursor.fetchall()
        spalten=[]
        for spalte in s: spalten.append(spalte[0])
        return spalten
    except: return None

def SQLqueryDB(conn,query):
    """SQLqueryDB(conn,query) perform an SQL query on a database and returns a table
    
    """
    cursor = conn.cursor()
    cursor.execute(query) 
    if None!=cursor.description:
        spNames=[x[0] for x in cursor.description]
        res=[spNames ]+map(list,cursor.fetchall()) 
    else: res=None
    cursor.close()
    return res


def getTableNames(conn):
    """getTableNames(conn) gets a list or names of the tables in DB
    
    """
    cursor = conn.cursor()
    #cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    cursor.execute("SHOW TABLES")
    s=cursor.fetchall()
    s=[x[0] for x in s]
    cursor.close()
    return map(str,s)


# Dialoge -------------------------------------------------------------

def SWColorDialogQ(): # Gibt QT-Farbe
    """SWColorDialogQ() open a dialog for choosing a color 
    
    Returns a PyQT Color object"""
    (f,ok)= QtGui.QColorDialog.getRgba()
    if not(ok): return None
    return  mkQCol(f)

def  SWColorDialog(): # Gibt Liste der RGB-Werte
    """SWColorDialog() opend a choose color dialog
    
    Returns a list of RGB values"""
    (f,ok)= QtGui.QColorDialog.getRgba()
    if not(ok): return None
    col=mkQCol(f)
    return [col.red(),col.green(),col.blue()]

def SWFileDialog(title="Select File",dir=None):
    """SWFileDialog(title="Select File",dir=None) - shows a file select dialog
    
    The optional argument dir specifies the start directory.
    Return value is a string (filename with path)"""
    if dir==None:
        s=str(QtGui.QFileDialog.getOpenFileName(caption=title))
        if s=="": return None
        else: return s
    else: 
        s=str(QtGui.QFileDialog.getOpenFileName(caption=title,directory=dir))
        if s=="": return None
        else: return s

def SWWarning(text): 
    """SWWarning(text) - shows a message box
    
    text may contain HTML tags"""
    if not(isinstance(text,str)): text=str(text)
    QtGui.QMessageBox.warning(TheWin,"SWWarning",text)

def SWYesNoDialog(text): # Liefert boolean
    """SWYesNoDialog(text) - shows a message box and yes/no question
    
    text may contain HTML tags. Returns True or False"""
    if not(isinstance(text,str)): text=str(text)
    return 0==QtGui.QMessageBox.question(TheWin,"?",text,"yes","no")


class SWPromptDialog(QtGui.QDialog):
    def __init__(self,question,initText):
        QtGui.QDialog.__init__(self)
        L=QtGui.QLabel(question)
        layout=QtGui.QVBoxLayout()
        layout.addWidget(L)
        self.tf=QtGui.QLineEdit()
        self.tf.setText(initText)
        layout.addWidget(self.tf)
        okButton=QtGui.QPushButton("OK")
        cancelButton=QtGui.QPushButton("cancel")
        buLayout=QtGui.QHBoxLayout()
        buLayout.addWidget(okButton)
        buLayout.addWidget(cancelButton)
        layout.addLayout(buLayout)
        self.setLayout(layout)
        self.connect(okButton,Qt.SIGNAL("clicked()"),self,Qt.SLOT("accept()"))
        self.connect(cancelButton,Qt.SIGNAL("clicked()"),self,Qt.SLOT("reject()"))
        self.setWindowTitle("Enter")
    def getText(self): return str(self.tf.text())

def SWTextDialog(question,initText="",oktest=None,converter=None):
    """SWTextDialog(question,initText="",oktest=None,converter=None)
    
    SWTextDialog opens a dialog that asks for a text string.
    initText, if given, is the text initially contaied in the field.
    optest, if given, is a function of oone argument that is called to
    check wheter the inpou is valid
    converter, if given, is a function that is applied before return.
    Example:  SWTextDialog('Enter number', converter=int) gives a number"""
    d=SWPromptDialog(question,initText)
    while True:
        if d.exec_()==0: return None
        r=d.getText()
        if oktest==None: 
            if converter==None: return r
            else: return converter(r)
        if oktest(r):
            if converter==None: return r
            else: return converter(r)
            
def isIntStr(s):
    try:
        i=int(s)
    except: return False
    return True
def isFloatStr(s):
    try:
        i=float(s)
    except: return False
    return True
    
def SWIntDialog(question,init=0):
    """SWIntDialog(question,init=0) ask for an Integer
    
    """
    return SWTextDialog(question,str(init),isIntStr,int)     

def SWFloatDialog(question,init=0.0):
    """SWFloatDialog(question,init=0.0) ask for a Floating point number
    
    """
    return SWTextDialog(question,str(init),isFloatStr,float)     


#- Bitmapgraphics

class SWImage(QtGui.QWidget):
    def __init__(self, width=None,height=None,container=None, file=None, dim=[200,200], parent=None):
        QtGui.QWidget.__init__(self,parent)
        if not(width==None) and not(height==None): dim=[width,height]
        self.pen = QtGui.QPen()
        self.brush = QtGui.QBrush()
        self.viewport=[-10,10,-10,10] # [xmin,xmax,ymin,ymax]
        if file!=None:
            self.image= QtGui.QImage(file)
            self.setMinimumWidth(self.image.width())
            self.setMinimumHeight(self.image.height())
            self.painter=QtGui.QPainter(self.image)
            self.painter.drawImage(0, 0, self.image,sx=0,sy=0)
            self.update()
            self.dim=[self.image.width(),self.image.height()]
        else:
            self.setMinimumWidth(dim[0])
            self.setMinimumHeight(dim[1])
            self.image= QtGui.QImage(dim[0],dim[1],4) # 4=RGB
            self.painter=QtGui.QPainter(self.image)
            self.image.fill(mkQColNum([255,255,255]))
            self.dim=dim
            self.update()
        self.myColor=mkQCol("black")
        if container==None: self.layout = TheCursor
        else: self.layout =container
        self.layout.addWidget(self)
        self.mousePressCommand=None
        self.mouseReleaseCommand=None
        self.mouseDragCommand=None
    def W2S(self,xy):
        assert isinstance(xy,list)
        assert len(xy)==2
        [xw,yw]=xy
        [xmin,xmax,ymin,ymax]=self.viewport
        return [int(float(self.getWidth())*float(xw-xmin)/float(xmax-xmin)),
                int(float(self.getHeight())*float(ymax-yw)/float(ymax-ymin))]
    def S2W(self,xy):
        assert isinstance(xy,list)
        assert len(xy)==2
        [xs,ys]=xy
        [xmin,xmax,ymin,ymax]=self.viewport
        return [xmin+(xmax-xmin)*xs/float(self.getWidth()),
                ymax-(ymax-ymin)*ys/float(self.getHeight())]
    def setActive(self,value):
        self.setUpdatesEnabled(value) 
        if value: self.update()
    def save(self,filename):
        """save(dateiname) speicher das Bild in einer Datei
        
        """
        self.image.save(filename)
    def minimumSizeHint(self): return QtCore.QSize(20, 20)
    #def sizeHint(self): return QtCore.QSize(400, 200)
    def paintEvent(self, event):
        painter=QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        painter.end()
    def getHeight(self): return self.image.height()    
    def getWidth(self): return self.image.width()
    def setColor(self,col): self.myColor=mkQCol(col)    
    def load(self,filename): 
        assert isinstance(filename,str)
        try:
            self.painter.end()
        except: pass
        self.image.load(filename)
        self.setMinimumWidth(self.image.width())
        self.setMinimumHeight(self.image.height())
        self.painter=QtGui.QPainter(self.image)
        self.painter.drawImage(0, 0, self.image,sx=0,sy=0)
        self.update()
    def getPixel(self, x, y):
        """getPixel(x,y)    Gibt eine [R,G,B]-Liste der Farbe an Position x,y
        
        """
        if isinstance(x,float): x=int(x)
        if isinstance(y,float): y=int(y)
        assert isinstance(x,int)
        assert isinstance(y,int)
        w=self.image.pixel(x,y)
        return [int((w/(256*256))%256), int((w/256)%256), int(w%256)]
    def getPixelGray(self, x, y):
        """getPixelGray(x,y)    Gibt den Helligkeitswert  der Farbe an Position x,y
        
        """
        if isinstance(x,float): x=int(x)
        if isinstance(y,float): y=int(y)
        assert isinstance(x,int)
        assert isinstance(y,int)
        col=QtGui.QColor(self.image.pixel(x,y))
        return (col.red()+col.green()+col.blue())/3
    def getPixelQ(self, x, y):
        """getPixelQ(x,y)    Gibt das QColor-Objekt der Farbe an Position x,y
        
        """
        return QtGui.QColor(self.image.pixel(x,y))
    def setPixelW(self,x,y,col=None):
        assert isinstance(x,int) or isinstance(x,float)
        assert isinstance(y,int) or isinstance(y,float)
        [xx,yy]=self.W2S([x,y])
        self.setPixel(xx,yy,col)
    def setPixel(self,x,y,col=None):
        """setPixel(x,y,farbe)
        
        Setzt die Farbe an Position x,y auf farbe (optional).""" 
        if isinstance(x,float): x=int(x)
        if isinstance(y,float): y=int(y)
        assert isinstance(x,int)
        assert isinstance(y,int)
        if col==None:
            self.image.setPixel(x,y,mkQColNum(self.myColor))
        if type(col)==list and len(col)==3:
            self.image.setPixel(x,y,int(256*256*256*255+256*256*col[0]+256*col[1]+col[2]))
        else:
            self.image.setPixel(x,y,mkQColNum(col))
    def fill(self,col=None):
        if col==None: self.image.fill(self.myColor)
        else: self.image.fill(mkQColNum(col))
    def drawPoint(self,x,y,col=None):
        if isinstance(x,float): x=int(x)
        if isinstance(y,float): y=int(y)
        assert isinstance(x,int)
        assert isinstance(y,int)
        if col==None: self.painter.setPen(self.myColor)
        else: self.painter.setPen(mkQCol(col))
        self.painter.drawPoint(x,y)
    def drawLine(self,x0,y0,x1,y1,col=None):
        if col==None: self.painter.setPen(self.myColor)
        else: self.painter.setPen(mkQCol(col))
        self.painter.drawLine(x0,y0,x1,y1)
    def drawLineW(self,x0,y0,x1,y1,col=None):
        [X0,Y0]=self.W2S([x0,y0])
        [X1,Y1]=self.W2S([x1,y1])
        self.drawLine(X0,Y0,X1,Y1,col)
    def drawCircleW(self,xm,ym,r,col=None,filled=False):
        [x,y]=self.W2S([xm,ym])
        x1=self.W2S([xm+r,ym])[0]
        y1=self.W2S([xm,ym+r])[1]
        rr=int(math.sqrt((x1-x)**2+(y1-y)**2))
        self.drawCircle(x,y,rr,col,filled)
    def drawCircle(self,xm,ym,r,col=None,filled=False): 
        self.drawEllipse(xm-r,ym-r,2*r,2*r,col,filled)
    def drawEllipse(self,x0,y0,xd,yd,col=None,filled=False): 
        if col==None: self.painter.setPen(self.myColor)
        else: self.painter.setPen(mkQCol(col))
        if filled and col==None: self.painter.setBrush(self.myColor)
        if filled and col!=None: self.painter.setBrush(mkQCol(col))
        if not(filled): 
            self.brush.setStyle(0)
            self.painter.setBrush(self.brush)
        self.painter.drawEllipse(x0,y0,xd,yd)
    def drawRectW(self,x0,y0,xd,yd,col=None,filled=False):
        [X0,Y0]=self.W2S([x0,y0])
        [X1,Y1]=self.W2S([x0+xd,y0+yd])
        self.drawRect(X0,Y0,X1-X0,Y1-Y0,col,filled)        
    def drawRect(self,x0,y0,xd,yd,col=None,filled=False): 
        if col==None: self.painter.setPen(self.myColor)
        else: self.painter.setPen(mkQCol(col))
        if filled and col==None: self.painter.setBrush(self.myColor)
        if filled and col!=None: self.painter.setBrush(mkQCol(col))
        if not(filled): 
            self.brush.setStyle(0)
            self.painter.setBrush(self.brush)
        self.painter.drawRect(x0,y0,xd,yd)
    def drawPolygon(self,coords,col=None,filled=False): 
        """drawPolygon(coords,col=None,filled=False)
        
        draws a polygon. Coordinates are either of the form [x1,y2],[x2,y],...] or [x1,y1,x2y2,...]"""
        if col==None: self.painter.setPen(self.myColor)
        else: self.painter.setPen(mkQCol(col))
        if filled and col==None: self.painter.setBrush(self.myColor)
        if filled and col!=None: self.painter.setBrush(mkQCol(col))
        if not(filled): 
            self.brush.setStyle(0)
            self.painter.setBrush(self.brush)
        self.painter.drawPolygon(QtGui.QPolygon(flattenList(coords)))
    def drawTextW(self,x0,y0,t,col=None):
        [x,y]=self.W2S([x0,y0])
        self.drawText(x,y,t,col)
    def drawText(self,x0,y0,t,col=None): 
        if col==None: self.painter.setPen(self.myColor)
        else: self.painter.setPen(mkQCol(col))
        self.painter.drawText(x0,y0,QtCore.QString(t))
    def getTurtle(self): return SWTurtle(self)
    # Eventhandler nehmen zwei Argumente: widget, event (mit X und Y Feldern)
    def setMousePressCommand(self,s): self.mousePressCommand=s
    def setMouseReleaseCommand(self,s): self.mouseReleaseCommand=s
    def setMouseDragCommand(self,s): self.mouseDragCommand=s
    def setMouseMoveCommand(self,s): self.mouseDragCommand=s
    def mousePressEvent(self, event): 
        if self.mousePressCommand!=None: 
            event.X=int(event.x())
            event.Y=int(event.y())
            self.mousePressCommand(self,event)
    def mouseReleaseEvent(self, event):
        if self.mouseReleaseCommand!=None: 
            event.X=int(event.x())
            event.Y=int(event.y())
            self.mouseReleaseCommand(self,event)
    def mouseMoveEvent(self, event):
        if self.mouseDragCommand!=None: 
            event.X=int(event.x())
            event.Y=int(event.y())
            self.mouseDragCommand(self,event)
    
class SWTurtle:
    def __init__(self,BM):
        """Erzeuge eine Turtle auf eienm SWImage

        BM ist eine Bitmap vom Typ SWImage"""
        self.BM=BM
        self.turtle=[BM.image.width()/2,BM.image.height()/2,0,True,
                     mkQColNum("black")]
    def left(self,alpha): 
        """Drehen der Turtle

        alpha ist der Drehwinkel"""
        assert isinstance(alpha,int) or isinstance(alpha,float)
        self.turtle[2]=self.turtle[2]-alpha
    def right(self,alpha): 
        """Drehen der Turtle

        alpha ist der Drehwinkel"""
        assert isinstance(alpha,int) or isinstance(alpha,float)
        self.turtle[2]=self.turtle[2]+alpha
    def setDirection(self,alpha): 
        """Drehen der Turtle

        alpha ist der Winkel gegen die Rechtsachse"""
        assert isinstance(alpha,int) or isinstance(alpha,float)
        self.turtle[2]=alpha
    def setPosition(self,x,y): 
        """Setzt die Position der Turtle ohne Zeichnen

        x,y sind die Zielkoordinaten (in Pixeln)"""
        self.turtle[0]=x
        self.turtle[1]=y
    def moveTo(self,x,y): 
        """Bewegt die Turtle

        x,y sind die Zielkoordinaten (in Pixeln)"""
        if isinstance(x,float): x=int(x)
        if isinstance(y,float): y=int(y)
        assert isinstance(x,int)
        assert isinstance(y,int)
        if self.turtle[3]:
            self.BM.drawLine(self.turtle[0],self.turtle[1],x,y,self.turtle[4])
        self.turtle[0]=x
        self.turtle[1]=y        
    def forward(self,L):
        """Bewegt die Turtle

        L ist die Distanz in Pixeln"""
        assert isinstance(L,int) or isinstance(L,float)
        [x0,y0,alpha,pd,col]=self.turtle
        x1=x0+L*math.cos(alpha/180.0*math.pi)
        y1=y0+L*math.sin(alpha/180.0*math.pi)
        self.turtle[0]=x1
        self.turtle[1]=y1
        if pd:
            self.BM.drawLine(x0,y0,x1,y1,col)
    def backward(self,L):
        """Bewegt die Turtle rueckwaerts

        L ist die Distanz in Pixeln"""
        assert isinstance(L,int) or isinstance(L,float)
        [x0,y0,alpha,pd,col]=self.turtle
        x1=x0-L*math.cos(-alpha/180.0*math.pi)
        y1=y0-L*math.sin(-alpha/180.0*math.pi)
        self.turtle[0]=x1
        self.turtle[1]=y1
        if self.turtle[3]:
            self.BM.drawLine(x0,y0,x1,y1,col)
    def penUp(self): 
        """Schaltet den Stift der Turtle aus"""
        self.turtle[3]=False
    def penDown(self): 
        """Schaltet den Stift der Turtle an"""
        self.turtle[3]=True
    def setPenColor(self,col): 
        """Setzt die Farbe der Turtle
        
        Die Farbe kann ein RGB-Tupel wie [255,0,0] oder ein Wort wie 'red' sein"""
        self.turtle[4]=mkQColNum(col)
    def setColor(self,col): 
        """Setzt die Farbe der Turtle (wie setPenColor)
        
        Die Farbe kann ein RGB-Tupel wie [255,0,0] oder ein Wort wie 'red' sein"""
        self.turtle[4]=mkQColNum(col)




# Item-bases graphics
# http://doc.qt.nokia.com/qq/qq19-graphicsview.html

# ToDo:
# - Events werden von image geschluckt.


class SWGraphics(QtGui.QGraphicsView):
    def __init__(self, width=200,height=200, dim=[], container=None,file=None):
        QtGui.QGraphicsView.__init__(self)
        if not(dim==[]): [width,height]=dim
        else: dim=[width,height]
        self.dim=dim
        self.allItems=[]
        self.scene=QtGui.QGraphicsScene()
        self.scene.setSceneRect(0,0,width,height)
        self.setScene(self.scene)
        self.pen = QtGui.QPen()
        self.brush = QtGui.QBrush()
        self.viewport=[-10,10,-10,10] # [xmin,xmax,ymin,ymax]
        self.penColor=mkQCol("black")
        self.myColor=mkQCol("black")
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        if container==None: self.layout = TheCursor
        else: self.layout =container
        self.layout.addWidget(self)
        # jetzt noch zwei ergaenzungen zur bm graphic
        if file==None:
            self.image= QtGui.QImage(width,height,4) # 4=RGB
            self.image.fill(mkQColNum([255,255,255]))
        else: 
            self.setBackgroundImage(file) 
        self.mousePressCommand=None
        self.mouseReleaseCommand=None
        self.mouseDragCommand=None
        self.painter=QtGui.QPainter(self.image)
        self.resize(QtCore.QSize(self.dim[0],self.dim[1]))
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        self.updateGeometry()
        self.update()
    def drawBackground(self,painter,rect): # Virtuelle Method aus QGraphicsView
        painter.drawImage(0, 0, self.image)
    def setBackgroundImage(self,f):
        if type(f)==str:
            self.image= QtGui.QImage(f)
            self.image=QtGui.QImage.convertToFormat (self.image,5) # KOnvertiert in Pixmap
            #self.setMinimumWidth(self.image.width())
            #self.setMinimumHeight(self.image.height())
            self.dim=[self.image.width(),self.image.height()]
            self.scene.setSceneRect(0,0,self.dim[0],self.dim[1])
            self.updateGeometry()
    # Start der neuen Methoden aus SWImage
    def setActive(self,value):
        self.setUpdatesEnabled(value) 
        if value: self.update()
    def save(self,filename):
        """save(dateiname) speicher das Bild in einer Datei
        
        """
        self.image.save(filename)
    def getHeight(self): return self.image.height()    
    def getWidth(self): return self.image.width()
    def setColor(self,col): self.myColor=mkQCol(col)    
    def load(self,filename): 
        assert isinstance(filename,str)
        try:
            self.painter.end()
        except: pass
        self.image.load(filename)
        self.setMinimumWidth(self.image.width())
        self.setMinimumHeight(self.image.height())
        self.painter=QtGui.QPainter(self.image)
        self.painter.drawImage(0, 0, self.image,sx=0,sy=0)
        self.update()
    def getPixel(self, x, y):
        """getPixel(x,y)    Gibt eine [R,G,B]-Liste der Farbe an Position x,y
        
        """
        if isinstance(x,float): x=int(x)
        if isinstance(y,float): y=int(y)
        assert isinstance(x,int)
        assert isinstance(y,int)
        w=self.image.pixel(x,y)
        return [int((w/(256*256))%256), int((w/256)%256), int(w%256)]
    def getPixelGray(self, x, y):
        """getPixelGray(x,y)    Gibt den Helligkeitswert  der Farbe an Position x,y
        
        """
        if isinstance(x,float): x=int(x)
        if isinstance(y,float): y=int(y)
        assert isinstance(x,int)
        assert isinstance(y,int)
        col=QtGui.QColor(self.image.pixel(x,y))
        return (col.red()+col.green()+col.blue())/3
    def getPixelQ(self, x, y):
        """getPixelQ(x,y)    Gibt das QColor-Objekt der Farbe an Position x,y
        
        """
        return QtGui.QColor(self.image.pixel(x,y))
    def setPixelW(self,x,y,col=None):
        assert isinstance(x,int) or isinstance(x,float)
        assert isinstance(y,int) or isinstance(y,float)
        [xx,yy]=self.W2S([x,y])
        self.setPixel(xx,yy,col)
    def setPixel(self,x,y,col=None):
        """setPixel(x,y,farbe)
        
        Setzt die Farbe an Position x,y auf farbe (optional).""" 
        if isinstance(x,float): x=int(x)
        if isinstance(y,float): y=int(y)
        assert isinstance(x,int)
        assert isinstance(y,int)
        if col==None:
            self.image.setPixel(x,y,mkQColNum(self.myColor))
        if type(col)==list and len(col)==3:
            self.image.setPixel(x,y,int(256*256*256*255+256*256*col[0]+256*col[1]+col[2]))
        else:
            self.image.setPixel(x,y,mkQColNum(col))
    def fill(self,col=None):
        if col==None: self.image.fill(self.myColor)
        else: self.image.fill(mkQColNum(col))
    def drawPoint(self,x,y,col=None):
        if isinstance(x,float): x=int(x)
        if isinstance(y,float): y=int(y)
        assert isinstance(x,int)
        assert isinstance(y,int)
        #painter=QtGui.QPainter(self.image)
        painter=self.painter
        if col==None: painter.setPen(self.myColor)
        else: painter.setPen(mkQCol(col))
        painter.drawPoint(x,y)
    def drawLine(self,x0,y0,x1,y1,col=None):
        #painter=QtGui.QPainter(self.image)
        painter=self.painter
        if col==None: self.painter.setPen(self.myColor)
        else: painter.setPen(mkQCol(col))
        painter.drawLine(x0,y0,x1,y1)
    def drawLineW(self,x0,y0,x1,y1,col=None):
        [X0,Y0]=self.W2S([x0,y0])
        [X1,Y1]=self.W2S([x1,y1])
        self.drawLine(X0,Y0,X1,Y1,col)
    def drawCircleW(self,xm,ym,r,col=None,filled=False):
        [x,y]=self.W2S([xm,ym])
        x1=self.W2S([xm+r,ym])[0]
        y1=self.W2S([xm,ym+r])[1]
        rr=int(math.sqrt((x1-x)**2+(y1-y)**2))
        self.drawCircle(x,y,rr,col,filled)
    def drawCircle(self,xm,ym,r,col=None,filled=False): 
        self.drawEllipse(xm-r,ym-r,2*r,2*r,col,filled)
    def drawEllipse(self,x0,y0,xd,yd,col=None,filled=False): 
        #painter=QtGui.QPainter(self.image)
        painter=self.painter
        if col==None: painter.setPen(self.myColor)
        else: painter.setPen(mkQCol(col))
        if filled and col==None: painter.setBrush(self.myColor)
        if filled and col!=None: painter.setBrush(mkQCol(col))
        if not(filled): 
            self.brush.setStyle(0)
            painter.setBrush(self.brush)
        painter.drawEllipse(x0,y0,xd,yd)
    def drawRectW(self,x0,y0,xd,yd,col=None,filled=False):
        [X0,Y0]=self.W2S([x0,y0])
        [X1,Y1]=self.W2S([x0+xd,y0+yd])
        self.drawRect(X0,Y0,X1-X0,Y1-Y0,col,filled)        
    def drawRectORIGINAL(self,x0,y0,xd,yd,col=None,filled=False): 
        #self.painter=QtGui.QPainter(self.image)
        if col==None: self.painter.setPen(self.myColor)
        else: self.painter.setPen(mkQCol(col))
        if filled and col==None: self.painter.setBrush(self.myColor)
        if filled and col!=None: self.painter.setBrush(mkQCol(col))
        if not(filled): 
            self.brush.setStyle(0)
            self.painter.setBrush(self.brush)
        self.painter.drawRect(x0,y0,xd,yd)
    def drawRect(self,x0,y0,xd,yd,col=None,filled=False): 
        if col==None: self.painter.setPen(self.myColor)
        else: self.painter.setPen(mkQCol(col))
        if filled and col==None: self.painter.setBrush(self.myColor)
        if filled and col!=None: self.painter.setBrush(mkQCol(col))
        if not(filled): 
            self.brush.setStyle(0)
            self.painter.setBrush(self.brush)
        self.painter.drawRect(x0,y0,xd,yd)
    def drawTextW(self,x0,y0,t,col=None):
        [x,y]=self.W2S([x0,y0])
        self.drawText(x,y,t,col)
    def drawText(self,x0,y0,t,col=None): 
        #self.painter=QtGui.QPainter(self.image)
        if col==None: self.painter.setPen(self.myColor)
        else: self.painter.setPen(mkQCol(col))
        self.painter.drawText(x0,y0,QtCore.QString(t))
    def getTurtle(self): return SWTurtle(self)
    # Ende der bm ergaenzung   #########################################
    def setPenColor(self,col): self.penColor=mkQCol(col)
    def getDim(self): return [self.scene.width(),self.scene.height()]
    def setViewport(self, vp): self.viewport=vp
    def xW2S(self,x): return float(self.scene.width()*(x-self.viewport[0])/
                                    float((self.viewport[1]-self.viewport[0])))
    def yW2S(self,y): return float(self.scene.height()*(1.0-(y-self.viewport[2])/
                                    float((self.viewport[3]-self.viewport[2]))))
    def xS2W(self,x): 
        return self.viewport[0]+x/float(self.scene.width())*(self.viewport[1]-self.viewport[0])
    def yS2W(self,y): 
        return self.viewport[2]+(self.scene.height()-y)/float(self.scene.height())*(self.viewport[3]-self.viewport[2])
    # Die 0-Varianten fuer Streckenlaengen,Radien u.a.
    def xW2S0(self,x): return float(self.scene.width()*x/float(self.viewport[1]-self.viewport[0]))
    def yW2S0(self,y): return float(self.scene.height()*y/float(self.viewport[3]-self.viewport[2]))
    def xS2W0(self,x): return x/float(self.scene.width())*(self.viewport[1]-self.viewport[0])
    def yS2W0(self,y): return (self.scene.height()-y)/float(self.scene.height())*(self.viewport[3]-self.viewport[2])
    def W2S(self,xy):
        assert isinstance(xy,list)
        assert len(xy)==2
        [xw,yw]=xy
        [xmin,xmax,ymin,ymax]=self.viewport
        return [float(self.scene.width())*float(xw-xmin)/float(xmax-xmin),
                float(self.scene.height())*float(ymax-yw)/float(ymax-ymin)]
    def S2W(self,xy):
        assert isinstance(xy,list)
        assert len(xy)==2
        [xs,ys]=xy
        [xmin,xmax,ymin,ymax]=self.viewport
        return [xmin+(xmax-xmin)*xs/float(self.scene.width()),
                ymax-(ymax-ymin)*ys/float(self.scene.height())]
    #def minimumSizeHint(self): return QtCore.QSize(self.scene.width(), self.scene.height())
    def sizeHint(self): 
        return QtCore.QSize(20+self.scene.width(), 20+self.scene.height())
    def minimumsizeHint(self):
        return QtCore.QSize(20+self.scene.width(), 20+self.scene.height())
    def add(self,obj): self.scene.addItem(obj)
    def addSWPixelImage(self,x,y,pixmap): # pixmap kann String (Datei) sein  
        pm=SWPixelImage(self,[x,y],pixmap)
        return pm
    def addLine(self,x1,y1,x2,y2,color=None):
        L=SWLine(self,[x1,y1,x2,y2])
        if color==None: L.setColor(mkQCol("black"))
        else: L.setColor(color)
        return L
    def addLineW(self,x1,y1,x2,y2,color=None):
        L=SWLine(self,[0,0,0,0])
        if color==None: L.setColor(mkQCol("black"))
        else: L.setColor(color)
        L.setCoordsW(x1,y1,x2,y2)
        return L
    def addRectangle(self,x,y,xd,yd,color=None,fillcolor=None):  
        re=SWRectangle(self,[x,y,xd,yd])
        re.setColor(color)
        re.setFillColor(fillcolor)
        return re
    def addRectangleW(self,x,y,xd,yd,color=None,fillcolor=None):  
        re=SWRectangle(self,[x,y,xd,yd],color=color,fillcolor=fillcolor)
        re.setColor(color)
        re.setFillColor(fillcolor)
        re.setCoordsW(x,y,xd,yd)
        return re
    def addEllipse(self,x,y,xd,yd,color=mkQCol("black"),fillcolor=None):  
        e=SWEllipse(self,[x,y,xd,yd])
        e.setColor(color)
        e.setFillColor(fillcolor)
        return e
    def addEllipseW(self,x,y,xd,yd,color=mkQCol("black"),fillcolor=None):  
        e=SWEllipse(self,[0,0,0,0])
        e.setColor(color)
        e.setFillColor(fillcolor)
        e.setCoordsW(x,y,xd,yd)
        return e
    def addCircle(self,x,y,r,color=mkQCol("black"),fillcolor=None):  
        e=SWEllipse(self,[x,y,r])
        e.setColor(color)
        e.setFillColor(fillcolor)
        return e
    def addCircleW(self,x,y,r,color=mkQCol("black"),fillcolor=None):  
        e=SWEllipse(self,[10,10,1])
        e.setColor(color)
        e.setFillColor(fillcolor)
        e.setCoordsW(x,y,r)
        return e
    def addPolygon(self,coords): 
        poly=QtGui.QPolygonF(map(lambda p: QtCore.QPointF(p[0],p[1]), coords))
        return self.scene.addPolygon(poly)
    def addFilledPolygon(self,coords): 
        poly=QtGui.QPolygonF(map(lambda p: QtCore.QPointF(p[0],p[1]), coords))
        return self.scene.addPolygon(poly,pen=self.pen,brush=self.brush)
    def addText(self,x,y,s): 
        assert isinstance(s,str)
        assert isinstance(x,int) or isinstance(x,float)
        t=self.scene.addText(s)
        t.setPos(x,y)
        return t
    def removeItem(self,obj): self.scene.removeItem(obj)
    def clear(self): 
        self.scene.clear()
        self.scene.update()
    def update(self): 
        self.scene.update()
    # Eventhandler nehmen zwei Argumente: widget, event (mit X und Y Feldern)
    def setMousePressCommand(self,s): self.mousePressCommand=s
    def setMouseReleaseCommand(self,s): self.mouseReleaseCommand=s
    def setMouseDragCommand(self,s): self.mouseDragCommand=s
    def setMouseMoveCommand(self,s): self.mouseDragCommand=s
    def mousePressEvent(self, event): 
        if self.mousePressCommand!=None: 
            event.X=int(event.x())
            event.Y=int(event.y())
            event.XW=self.xS2W(event.X)
            event.YW=self.yS2W(event.Y)
            if self.mousePressCommand.func_code.co_argcount==2:
                self.mousePressCommand(self,event)
            if self.mousePressCommand.func_code.co_argcount==1:
                self.mousePressCommand(event)
        QtGui.QGraphicsView.mousePressEvent(self, event)
    def mouseReleaseEvent(self, event):
        if self.mouseReleaseCommand!=None: 
            event.X=int(event.x())
            event.Y=int(event.y())
            event.XW=self.xS2W(event.X)
            event.YW=self.yS2W(event.Y)
            if self.mouseReleaseCommand.func_code.co_argcount==2:
                self.mouseReleaseCommand(self,event)
            if self.mouseReleaseCommand.func_code.co_argcount==2:
                self.mouseReleaseCommand(event)
            if not(self.mouseReleaseCommand.func_code.co_argcount in  [1,2]):
                raise(Exception("setMouseReleaseCommand must set function with one argument (event) or two (graphics,event)"))
        QtGui.QGraphicsView.mouseReleaseEvent(self, event)
    def mouseMoveEvent(self, event):
        if self.mouseDragCommand!=None: 
            try:
                event.X=int(event.x())
                event.Y=int(event.y())
                event.XW=self.xS2W(event.X)
                event.YW=self.yS2W(event.Y)
                self.mouseDragCommand(self,event)
            except: 
                try:
                    self.mouseDragCommand(event)
                except:
                    print "Fehler in mouseMoveEvent"
        QtGui.QGraphicsView.mouseMoveEvent(self, event)




#----------------------------------------------------------------------------

class SWGraphicsItem(QtGui.QGraphicsItem):
    def __init__(self,G):
        self.alpha=0
        self.SWG=G 
        self.SWG.allItems.append(self)
        self.autoDrag=False
        self.col=mkQCol("black")
        self.fillcolor=None
        self.filled=False
        self.collissionCommand=None
    def getDim(self): return  [self.boundingRect().width(), self.boundingRect().height()]
    def getDimW(self): return  [self.SWG.xW2S0(self.boundingRect().width()), 
                                self.SWG.yW2S0(self.boundingRect().height())]
    def setDimW(self,xy): # Center fixed
        self.setDim([self.SWG.xW2S0(xy[0]),self.SWG.yW2S0(xy[1])])
    def setDim(self,xy):
        [cx,cy]=self.getCenter()
        self.setRect(cx-xy[0]/2,cy-xy[1]/2,xy[0],xy[1])
    def setRect___(self,*args):
        if len(args)==1:
            if isinstance(args[0],QtCore.QRect) or isinstance(args[0],QtCore.QRectF): 
                self.setPos(args[0].topLeft())
                self.scale(args[0].width()/float(self.boundingRect().widtht()),
                           args[0].height()/float(self.boundingRect().height()))
                self.update()
                return
        if len(args)==4:
            self.setPos(args[0],args[1])
            self.scale(args[2]/float(self.boundingRect().widtht()),
                       args[3]/float(self.boundingRect().height()))
            self.update()
            return
        print "SWGraphicsItem.setRect ignored! args=",args
                        
    # Jetzt Zentrum
    def getCenter(self): 
        p=self.boundingRect().center()
        return [p.x(),p.y()]
    def getCenterW(self): 
        p=self.boundingRect().center()
        return [self.SWG.xS2W(p.x()),self.SWG.yS2W(p.y())]
    def getX(self): return self.getCenter()[0]
    def getY(self): return self.getCenter()[1]
    def getX(self): return self.pos().x()+self.boundingRect().width()/2
    def getY(self): return self.pos().y()+self.boundingRect().width()/2
    def getXW(self): return self.getCenterW()[0]
    def getYW(self): return self.getCenterW()[1]
    # jetzt links obenn
    def getPos(self): return list(self.boundingRect().getCoords())[0:2] #Position links oben
    def getPosW(self): return self.SWG.S2W(list(self.boundingRect().getCoords())[0:2])
    def getX1(self): return list(self.boundingRect().getCoords())[0]
    def getY1(self): return list(self.boundingRect().getCoords())[1]
    def getX1W(self): return self.SWG.xS2W(list(self.boundingRect().getCoords())[0])
    def getY1W(self): return self.SWG.yS2W(list(self.boundingRect().getCoords())[1])
    def setCenter(self,*args): 
        if len(args)==2: xy=list(args)
        else: 
            if len(args)==1 and type(args[0])==list: xy=args[0]
            else: xy=[0,0]
        x=self.boundingRect().x()
        y=self.boundingRect().y()
        w=self.boundingRect().width()
        h=self.boundingRect().height()
        p=self.boundingRect().center()
        [xc,yc]=[p.x(),p.y()]
        [dx,dy]=[xy[0]-xc,xy[1]-yc]
        self.setRect(QtCore.QRectF(x+dx,y+dy,w,h))
        self.handleCollide()
    def setCenterW(self,*args):
        if len(args)==2: xy=list(args)
        else: 
            if len(args)==1 and type(args[0])==list: xy=args[0]
            else: xy=[0,0]
        xy=self.SWG.W2S(xy)
        apply(self.setCenter,xy)
        self.handleCollide()
    def setPosW(self,*args):
        if len(args)==2: xy=list(args)
        else: 
            if len(args)==1 and type(args[0])==list: xy=args[0]
            else: xy=[0,0]
        xy=self.SWG.W2S(xy)
        apply(self.setPos,xy)
        self.handleCollide()
    def setPos(self,*args): 
        if len(args)==2: xy=list(args)
        else: 
            if len(args)==1 and type(args[0])==list: xy=args[0]
            else: xy=[0,0]
        w=self.boundingRect().width()
        h=self.boundingRect().height()
        self.setRect(QtCore.QRectF(xy[0],xy[1],w,h))
        self.handleCollide()
    def moveTo(self,x,y): 
        self.setCenter(x,y)
    def moveToW(self,x,y): self.setCenterW(x,y)
    def move(self,dx,dy): 
        self.moveBy(dx,dy)
        self.handleCollide()
    def moveW(self,dx,dy): self.moveBy(self.SWG.xW2S0(dx),self.SWG.yW2S0(dy))
    # jetzt rechts unten
    def getX2(self): return list(self.boundingRect().getCoords())[2]+self.getX1()
    def getY2(self): return list(self.boundingRect().getCoords())[3]+self.getY1()
    def getX2W(self): return self.SWG.xS2W0(list(self.boundingRect().getCoords())[2])+self.getY1W()
    def getY2W(self): return self.SWG.yS2W0(list(self.boundingRect().getCoords())[3])+self.getY1W()
    # gibt Coords gibt i.a. x1,y1 x2,y2 aus, wird ggf überladen
    def getCoords(self): return self.getPos()+vectorAdd(self.getPos(),self.getDim())
    def getCoordsW(self): return self.getPosW()+vectorAdd(self.getPosW(),self.getDimW())
    def getWidth(self): return self.getDim()[0]
    def getHeight(self): return self.getDim()[1]
    def getWidthW(self): return self.SWG.xW2S0(self.getDim()[0])
    def getHeightW(self): return self.SWG.yW2S0(self.getDim()[1])
    def Rotate(self,winkel): # Winkel in Grad
        self.alpha+=winkel
        [x,y]=self.getCenter()
        self.setTransform(QtGui.QTransform().translate(x, y).rotate(self.alpha).translate(-x, -y))
    def handleCollide(self):
        if self.collissionCommand==None: return
        cl=self.MycollidingItems()
        #print "collidng ",str(cl)," out of "+str(self.SWG.allItems)
        if cl==[]: return
        self.collissionCommand(cl)
    def setCollissionCommand(self,cmd): 
        self.collissionCommand=cmd
    def MycollidingItems(self):
        res=[]
        for obj in self.SWG.allItems:
            if obj.collidesWithItem(self): res.append(obj)
        return res
    def setAutoDrag(self,yesNo): self.autoDrag=yesNo
    def setMousePressCommand(self,s): self.mousePressCommand=s
    def setMouseReleaseCommand(self,s): self.mouseReleaseCommand=s
    def setMouseDragCommand(self,s): self.mouseDragCommand=s
    def setMouseMoveCommand(self,s): self.mouseDragCommand=s
    def mousePressEvent(self, event):
        if self.mousePressCommand!=None: 
            pos=map(int,[event.scenePos().x(),event.scenePos().y()])
            [event.X,event.Y]=pos
            [event.XW,event.YW]=[self.SWG.xS2W(pos[0]),self.SWG.yS2W(pos[1])]
            self.mousePressCommand(self,event)
    def mouseReleaseEvent(self, event):
        if self.mouseReleaseCommand!=None: 
            pos=map(int,[event.scenePos().x(),event.scenePos().y()])
            [event.X,event.Y]=pos
            [event.XW,event.YW]=[self.SWG.xS2W(pos[0]),self.SWG.yS2W(pos[1])]
            self.mouseReleaseCommand(self,event)
    def mouseMoveEvent(self, event):
        if self.autoDrag: 
           apply(self.setCenter,map(int,[event.scenePos().x(),event.scenePos().y()]))
        if self.mouseDragCommand!=None: 
            pos=map(int,[event.scenePos().x(),event.scenePos().y()])
            [event.X,event.Y]=pos
            [event.XW,event.YW]=[self.SWG.xS2W(pos[0]),self.SWG.yS2W(pos[1])]
            self.mouseDragCommand(self,event)
            self.SWG.update()
    def setColor(self,col): 
        if col==None:
            self.setPen(Qt.QColor(0,0,0,0))
        else:
            self.col=mkQCol(col)
            self.setPen(self.col)
    def setFillColor(self,col): # None erlaubt
        if col!=None: 
            self.fillcolor=mkQCol(col)
            self.filled=True
            self.setBrush(self.fillcolor)
            self.brush().setStyle(1)
        else: 
            self.filled=False
            self.setBrush(Qt.QColor(0,0,0,0))
    def setFilled(self,b): 
        self.filled=b




class SWEllipse(QtGui.QGraphicsEllipseItem,SWGraphicsItem):
    # Die Koordinaten sind Mittelpunkte und Radien
    def __init__(self,SWG,coords,mousePressCommand=None, mouseReleaseCommand=None,
                 mouseDragCommand=None):
        self.SWG=SWG
        self.scene=SWG.scene
        self.setMousePressCommand(mousePressCommand)
        self.setMouseReleaseCommand(mouseReleaseCommand)
        self.setMouseDragCommand(mouseDragCommand)
        if len(coords)==3: coords=coords+[coords[-1]]                
        QtGui.QGraphicsEllipseItem.__init__(self,coords[0]-coords[2],coords[1]-coords[3],
                                            2*coords[2],2*coords[3],scene=SWG.scene,parent=None)
        SWGraphicsItem.__init__(self,SWG)
    def setRadius(self,r): self.setDim([2*r,2*r])
    def setRadiusW(self,r): self.setDimW([2*r,2*r])
    def setRadii(self,rx,ry): self.setDim([2*rx,2*ry])
    def setRadiiW(self,rx,ry): self.setDimW([2*rx,2*ry])
    def setCoords(self,*args):
        if len(args)==3: 
            coords=list(args)
            coords=coords+[coords[-1]]
        else:
            if len(args)==4: coords=list(args)
            else: 
                if len(args)==2: coords=args+self.coords[2:]
                else: coords=args[0]
        self.setCenter(coords[0:2])
        self.setRadii(coords[2],coords[3])
        self.handleCollide()
    def setCoordsW(self,*args):
        if len(args)==3: 
            coordsW=list(args)
            coordsW=coordsW+[coordsW[-1]]
        else:
            if len(args)==4: coordsW=list(args)
            else: coordsW=args[0]
        self.setCenterW(coordsW[0:2])
        self.setRadiiW(coordsW[2],coordsW[3])
        self.handleCollide()


class SWRectangle(QtGui.QGraphicsRectItem,SWGraphicsItem):
    # Die Koordinaten sind Mittelpunkte und Radien
    def __init__(self,SWG,coords,mousePressCommand=None, mouseReleaseCommand=None,
                 mouseDragCommand=None):
        self.SWG=SWG
        self.scene=SWG.scene
        self.setMousePressCommand(mousePressCommand)
        self.setMouseReleaseCommand(mouseReleaseCommand)
        self.setMouseDragCommand(mouseDragCommand)
        if len(coords)==3: coords=coords+[coords[-1]]                
        QtGui.QGraphicsRectItem.__init__(self,coords[0]-coords[2],coords[1]-coords[3],
                                            2*coords[2],2*coords[3],scene=SWG.scene,parent=None)
        SWGraphicsItem.__init__(self,SWG)
    def setCoords(self,*args):
        if len(args)==3: 
            coords=list(args)
            coords=coords+[coords[-1]]
        else:
            if len(args)==4: coords=list(args)
            else: 
                if len(args)==2: coords=args+self.coords[2:]
                else: coords=args[0]
        coords=map(int,coords)
        [self.X,self.Y,self.Rx,self.Ry]=self.coords
        self.coords=coords
        self.calcWfromS()
        re=[self.coords[0]-self.coords[2],
                     self.coords[1]-self.coords[2],
                        2*self.coords[2], 2*self.coords[3]]
        #self.setRect(re)
        self.setRect(apply(self.mapRectFromScene,re))
        self.handleCollide()
    def setCoordsW(self,*args):
        if len(args)==3: 
            coordsW=list(args)
            coordsW=coordsW+[coordsW[-1]]
        else:
            if len(args)==4: coordsW=list(args)
            else: coordsW=args[0]
        self.coordsW=coordsW
        self.calcSfromW()
        re=[self.coords[0]-self.coords[2],
                     self.coords[1]-self.coords[2],
                        2*self.coords[2], 2*self.coords[3]]
        #self.setRect(re)
        self.setRect(apply(self.mapRectFromScene,re))
        self.handleCollide()
 



class SWLine(QtGui.QGraphicsLineItem,SWGraphicsItem):
    # Die Koordinaten sind Mittelpunkte und Radien
    def __init__(self,SWG,coords,mousePressCommand=None, mouseReleaseCommand=None,
                 mouseDragCommand=None,color=None):
        self.SWG=SWG
        self.scene=SWG.scene
        self.setMousePressCommand(mousePressCommand)
        self.setMouseReleaseCommand(mouseReleaseCommand)
        self.setMouseDragCommand(mouseDragCommand)
        QtGui.QGraphicsLineItem.__init__(self,coords[0],coords[1],coords[2],coords[3],scene=SWG.scene,parent=None)
        SWGraphicsItem.__init__(self,SWG)
    def setPos(self,x,y): self.setCenter(x,y)
    def setPosW(self,x,y): self.setCenterW(x,y)
    def setCoords(self,*args):
        if len(args)==4: coords=list(args)
        else: 
            if len(args)==2: coords=args+self.coords[2:]
            else: coords=args[0]
        self.setLine(self.coords[0],self.coords[1],
                     self.coords[2],self.coords[3])
        self.handleCollide()
    def setCoordsW(self,*args):
        if len(args)==4: coordsW=list(args)
        else: coordsW=args[0]
        
        self.setLine(self.SWG.xW2S(coordsW[0]),self.SWG.yW2S(coordsW[1]),
                     self.SWG.xW2S(coordsW[2]),self.SWG.yW2S(coordsW[3]))
        self.handleCollide()




class SWPixelImage(QtGui.QGraphicsPixmapItem,SWGraphicsItem):
    # Die Koordinaten sind Mittelpunkte 
    def __init__(self,SWG,coords,pixmap,mousePressCommand=None, mouseReleaseCommand=None,
                 mouseDragCommand=None):
        self.SWG=SWG
        self.scene=SWG.scene
        self.setMousePressCommand(mousePressCommand)
        self.setMouseReleaseCommand(mouseReleaseCommand)
        self.setMouseDragCommand(mouseDragCommand)
        self.autoDrag=False
        self.image=None
        if type(pixmap)==str: # Erzeugung aus Datei mit Namen
            pm=QtGui.QPixmap()
            self.image=QtGui.QImage(pixmap)
            pm.convertFromImage(self.image)
            pixmap=pm
        if not(isinstance(pixmap,QtGui.QPixmap)):
            raise Exception("QPixMap required")
        self.pixmap=pixmap
        if self.image==None: self.image=pixmap.toImage()
        QtGui.QGraphicsPixmapItem.__init__(self,pixmap,scene=SWG.scene,parent=None)
        SWGraphicsItem.__init__(self,SWG)
        self.setPos(coords)
#    def getCenter(self): 
#        p=self.boundingRect().center()
#        return [p.x(),p.y()]
#    def getX(self): return self.getCenter()[0]
#    def getY(self): return self.getCenter()[1]
    def dim(self): return [self.image.width(),self.image.height()]
    def setPosW(self,*args):
        if len(args)==2: xy=list(args)
        else: 
            if len(args)==1 and type(args[0])==list: xy=args[0]
            else: xy=[0,0]
        xy=self.SWG.W2S(xy)
        apply(self.setPos,xy)
        self.handleCollide()
    def setPos(self,*args): 
        if len(args)==2: xy=list(args)
        else: 
            if len(args)==1 and type(args[0])==list: xy=args[0]
            else: xy=[0,0]
        w=self.boundingRect().width()
        h=self.boundingRect().height()
        QtGui.QGraphicsPixmapItem.setPos(self,xy[0],xy[1])
        #self.setRect(QtCore.QRectF(xy[0],xy[1],w,h))
        self.handleCollide()
    def setPixel(self,x,y,col=None):
        """setPixel(x,y,farbe)
        
        Setzt die Farbe an Position x,y auf farbe (optional).""" 
        if isinstance(x,float): x=int(x)
        if isinstance(y,float): y=int(y)
        assert isinstance(x,int)
        assert isinstance(y,int)
        if col==None:
            self.image.setPixel(x,y,mkQColNum(self.myColor))
        if type(col)==list and len(col)==3:
            self.image.setPixel(x,y,int(256*256*256*255+256*256*col[0]+256*col[1]+col[2]))
        else:
            self.image.setPixel(x,y,mkQColNum(col))
        self.setPixmap(QtGui.QPixmap(self.image))




######################################################################

import traceback

class SWConsole(QtGui.QPlainTextEdit):
    def __init__(self, container=None, env={}, prompt='>>> ', 
                 startup_message='', parent=None):
        QtGui.QPlainTextEdit.__init__(self, parent)
        self.prompt = prompt
        self.history = []
        self.namespace = env
        self.construct = []
        if container==None: self.layout = TheCursor
        else: self.layout =container
        self.layout.addWidget(self)

        self.setGeometry(50, 75, 600, 400)
        self.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)
        self.setUndoRedoEnabled(False)
        self.document().setDefaultFont(QtGui.QFont("monospace", 10, QtGui.QFont.Normal))
        self.showMessage(startup_message)

    def updateNamespace(self, namespace):
        self.namespace.update(namespace)

    def showMessage(self, message):
        self.appendPlainText(message)
        self.newPrompt()

    def newPrompt(self):
        if self.construct:
            prompt = '.' * len(self.prompt)
        else:
            prompt = self.prompt
        self.appendPlainText(prompt)
        self.moveCursor(QtGui.QTextCursor.End)

    def getCommand(self):
        doc = self.document()
        curr_line = unicode(doc.findBlockByLineNumber(doc.lineCount() - 1).text())
        curr_line = curr_line.rstrip()
        curr_line = curr_line[len(self.prompt):]
        return curr_line

    def setCommand(self, command):
        if self.getCommand() == command:
            return
        self.moveCursor(QtGui.QTextCursor.End)
        self.moveCursor(QtGui.QTextCursor.StartOfLine, QtGui.QTextCursor.KeepAnchor)
        for i in range(len(self.prompt)):
            self.moveCursor(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor)
        self.textCursor().removeSelectedText()
        self.textCursor().insertText(command)
        self.moveCursor(QtGui.QTextCursor.End)

    def getConstruct(self, command):
        if self.construct:
            prev_command = self.construct[-1]
            self.construct.append(command)
            if not prev_command and not command:
                ret_val = '\n'.join(self.construct)
                self.construct = []
                return ret_val
            else:
                return ''
        else:
            if command and command[-1] == (':'):
                self.construct.append(command)
                return ''
            else:
                return command

    def getHistory(self):
        return self.history

    def setHisory(self, history):
        self.history = history

    def addToHistory(self, command):
        if command and (not self.history or self.history[-1] != command):
            self.history.append(command)
        self.history_index = len(self.history)

    def getPrevHistoryEntry(self):
        if self.history:
            self.history_index = max(0, self.history_index - 1)
            return self.history[self.history_index]
        return ''

    def getNextHistoryEntry(self):
        if self.history:
            hist_len = len(self.history)
            self.history_index = min(hist_len, self.history_index + 1)
            if self.history_index < hist_len:
                return self.history[self.history_index]
        return ''

    def getCursorPosition(self):
        return self.textCursor().columnNumber() - len(self.prompt)

    def setCursorPosition(self, position):
        self.moveCursor(QtGui.QTextCursor.StartOfLine)
        for i in range(len(self.prompt) + position):
            self.moveCursor(QtGui.QTextCursor.Right)

    def runCommand(self):
        command = self.getCommand()
        self.addToHistory(command)

        command = self.getConstruct(command)
        if command:
            tmp_stdout = sys.stdout

            class stdoutProxy():
                def __init__(self, write_func):
                    self.write_func = write_func
                    self.skip = False

                def write(self, text):
                    if not self.skip:
                        stripped_text = text.rstrip('\n')
                        self.write_func(stripped_text)
                        QtCore.QCoreApplication.processEvents()
                    self.skip = not self.skip

            sys.stdout = stdoutProxy(self.appendPlainText)
            try:
                try:
                    G=globals()
                    for g in G: 
                        self.namespace[g]==G[g]
                    result = eval(command, self.namespace, self.namespace)
                    if result != None:
                        self.appendPlainText(repr(result))
                except SyntaxError:
                    exec command in self.namespace
            except SystemExit:
                self.close()
            except:
                traceback_lines = traceback.format_exc().split('\n')
                # Remove traceback mentioning this file, and a linebreak
                for i in (3,2,1,-1):
                    traceback_lines.pop(i)
                self.appendPlainText('\n'.join(traceback_lines))
            sys.stdout = tmp_stdout
        self.newPrompt()

    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
            self.runCommand()
            return
        if event.key() == QtCore.Qt.Key_Home:
            self.setCursorPosition(0)
            return
        if event.key() == QtCore.Qt.Key_PageUp:
            return
        elif event.key() in (QtCore.Qt.Key_Left, QtCore.Qt.Key_Backspace):
            if self.getCursorPosition() == 0:
                return
        elif event.key() == QtCore.Qt.Key_Up:
            self.setCommand(self.getPrevHistoryEntry())
            return
        elif event.key() == QtCore.Qt.Key_Down:
            self.setCommand(self.getNextHistoryEntry())
            return
        elif event.key() == QtCore.Qt.Key_D and event.modifiers() == QtCore.Qt.ControlModifier:
            self.close()
        super(SWConsole, self).keyPressEvent(event)

welcome_message = '''
   ---------------------------------------------------------------
     Welcome to a primitive Python interpreter.
   ---------------------------------------------------------------
'''


#---------------------

def flattenList(L):
    R=[]
    for x in L:
        if type(x)==list: R=R+x
        else: R.append(x)
    return R

def testListType(L,t):
    if type(L)!=list: return False
    for x in L:
        if type(x)!=t: return False
    return True
def testListPred(L,p):
    if type(L)!=list: return False
    for x in L:
        if not(p(x)): return False
    return True

def vectorAdd(a,b):
    assert(type(a)==list)
    assert(type(b)==list)
    assert(len(a)==len(b))
    return [a[i]+b[i] for i in range(len(a))]
def vectorSub(a,b):
    assert(type(a)==list)
    assert(type(b)==list)
    assert(len(a)==len(b))
    return [a[i]-b[i] for i in range(len(a))]
def vectorSmul(s,a): return [s*x for x in a]
def scalarProduct(a,b): 
    assert(type(a)==list)
    assert(type(b)==list)
    assert(len(a)==len(b))
    return sum([a[i]*b[i] for i in range(len(a))])

#-----------------------


print "SWGui V2.1.3 - 31.08.2012"


#------------------------- Thread support
SWThreadList=[]

def Qsleep(seconds): QtCore.QThread.msleep(int(1000*seconds))

def ThreadExecute(fun,*args):
    """ThreadExecute(f,*argumente) fuehrt Funktion in neuem Thread aus
    
    Beispiel:  ThreadExecute(f) oder ThreadExecute(f,5,"text")
    f darf nicht due GUI veraendern!   """ 
    global SWThreadList
    t=SWThread(fun,list(args))
    SWThreadList.append(t)
    t.start()
class SWThread(QtCore.QThread):
    def __init__(self,fun,args):
        QtCore.QThread.__init__(self)
        self.fun=fun
        self.args=args
    def run(self):
        return apply(self.fun,self.args)




#SWinteract()
#TheMainWin.show()


