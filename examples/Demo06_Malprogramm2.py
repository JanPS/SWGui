from SWGui import *

SWLabel("Malprogramm")
BM=SWGraphics(dim=[400,200])
def zeichneSpur(bitmap,event):
    bitmap.drawPoint(event.X,event.Y,"red")
    c.setCenter(event.X,event.Y)
    bitmap.update()
BM.setMouseMoveCommand(zeichneSpur)
c=BM.addCircle(10,10,5)

SWstart()

