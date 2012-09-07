from SWGui import *
import time 
import thread

SWLabel("Scratchlike")
punkteLabel=SWLabel("0 Punkte")

G=SWGraphics(600,600)


Katze=G.addSWPixelImage(100,100,"img/cat1-a.gif")
Katze.setAutoDrag(True)

Maus=G.addSWPixelImage(200,400,"img/cub1.png")
Maus.setAutoDrag(True)
Maus.scale(0.5, 0.5)

print Maus

def MausProc():
    dx=7
    dy=4
    while True:
        time.sleep(0.1)
        print "---",Maus, Maus.getX(),Maus.getY()
        if Maus==None: continue
        Maus.move(dx,dy)
        if Maus.getX()>600 or Maus.getX()<0: 
            dx=-dx
            Maus.move(10*dx,0)
            Maus.scale(-1,1)
        if Maus.getY()>600 or Maus.getY()<0: 
            dy=-dy
            Maus.move(0,10*dy)
            Maus.scale(-1,1)

def kl(): Katze.move(-30,0)
def kr(): Katze.move(30,0)
def ko(): Katze.move(0,-30)
def ku(): Katze.move(0,30)

setKeyCommand("a",kl)            
setKeyCommand("s",kr)            
setKeyCommand("w",ko)            
setKeyCommand("y",ku)            

punkte=0
def KatzenStoss(L):
    global punkte
    if Maus in L: 
        punkte=punkte+1
        punkteLabel.setText(str(punkte)+" Punkte")
    
Katze.setCollissionCommand(KatzenStoss) 
        
ThreadExecute(MausProc)

SWstart()



 
    
