from SWGui import *

SWLabel("Malprogramm 2")
BM=SWGraphics(dim=[350,350])
print "Dimension: b=",BM.getWidth(), "h=", BM.getHeight()
for i in range(100): BM.setPixel(i,i*i/100,[255-i,0,3*i])
BM.drawLine(100,100,150,100,"green")
BM.drawText(100,130,"Das ist Text")
BM.drawEllipse(150,130,20,20)
BM.setColor("red")
BM.drawRect(200,200,20,30)
BM.drawRect(240,210,20,30,"yellow",True)
BM.setColor("blue")
BM.drawRect(230,230,20,30)
for w in range(360): 
    BM.drawPoint(200+50*math.cos(w/180.0*math.pi),
                200+50*math.sin(w/180.0*math.pi))
BM.drawText(50,190,"Hallo",[0,255,0])
BM.update()

SWstart()
