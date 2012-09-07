# -*- coding: utf-8 -*-

from SWGui import *

SWLabel("<b>Textfelder</b>")
tf=SWTextField()
l=SWLabel()
e=SWLabel()
def klick(): l.setText(tf.getText()) 
tf.setCommand(klick)

def edit(s): e.setText("jetzt: "+s)
tf.setChangeCommand(edit)

def tastendruck(key):
    print "Tastennummer: "+str(key) 
def tastendruckC(t):
    print "Tastenbeschriftung: "+t 
    
tf.setKeyCommand(tastendruck) 
tf.setKeyCCommand(tastendruckC) 
 
SWButton("clear",command=lambda: l.setText(""))

tf.setBackgroundColor("yellow")

SWstart()


