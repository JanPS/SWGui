# -*- coding: utf-8 -*-

from SWGui import *

def testEvent(*args): print ["Test-Event",args]
def buEvent(): print "Buttonklick!"
def cbComm(*args): print "Check-Box :" ,args
def handler1(a): print   "Haendler1 ",a
def handler2(a,b): print "Haendler2 ",a,b
def bu3h(a): print "Der Button ist ",a

b1=SWButton(text="Button1",command=buEvent)
b2=SWButton(text=u"Drücken",command=testEvent)
b3=SWButton(text="oder hier",command=bu3h)
cb1=SWCheckBox("Turbo",command=handler1)
cb2=SWCheckBox("Bremse",command=handler2)
SWHBox()
SWLabel(u"Hallöchen")
SWLabel("<b>Welt</b>")
SWLabel("<font color=#ff0000>rot</font> und schwarz")

# Wenn das Programm nicht interaktiv ausgefuehrt werden soll, 
# sollte die folgende Zeile ausgefuehrt werden:

SWstart()


