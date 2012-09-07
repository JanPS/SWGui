from SWGui import *

SWLabel("Malprogramm")
BM=SWImage(dim=[400,200])
def zeichneSpur(bitmap,event):
    bitmap.drawPoint(event.X,event.Y,"red")
    bitmap.update()
BM.setMouseMoveCommand(zeichneSpur)
SWstart()

