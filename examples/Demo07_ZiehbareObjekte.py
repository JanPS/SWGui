from SWGui import *


SWLabel("GrafikObjekte")
G=SWGraphics(400,400)
G.setPenColor([255,0,0])
G.addLine(-50,0,100,0)
R=G.addRectangle(200,130,40,50,color="blue")
R.setFillColor([100,100,255])
R.setFilled(True)

ell=G.addEllipse(30,100,20,20)
ell.setFilled(True)

L=G.addLine(100,100,200,100,color="red")
L.setAutoDrag(True)


def tP(obj,event): print "Event press:",[event.X,event.Y]
def tD(obj,event): print "Event DRAG:",[event.X,event.Y]
def tR(obj,event): print "Event release:",[event.X,event.Y]
def tkm(obj,event): 
    print "scenerect=",G.scene.sceneRect()
    print "Circle move:",[event.X,event.Y]
k3=G.addCircle(180,150,20,color="red")
k3.setAutoDrag(True)
e=G.addEllipse(0,0,20,50)
e.setFillColor("blue")
e.setMousePressCommand(tP)
e.setMouseDragCommand(tD)
e.setMouseReleaseCommand(tR)
e.setAutoDrag(True)


k=G.addCircle(150,180,20)
k.setColor("cyan")
k.setAutoDrag(True)
k.setMouseMoveCommand(tkm)

G.setPenColor([0,255,0])
k2=G.addCircle(0,0,80)
k.setColor("green")
k2.setAutoDrag(True)
k2.pen().color().setRed(255)

e2=G.addEllipse(100,150,70,20)
e2.setAutoDrag(True)
e2.setColor("yellow")

SWstart()
  