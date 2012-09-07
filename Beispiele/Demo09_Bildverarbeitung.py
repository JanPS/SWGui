from SWGui import *

SWLabel("Bildbearbeitungsprogramm")
BM=SWImage(file="img/bild1.jpg")
BM.update()
def negativ():
    for x in range(BM.getWidth()):
       for y in range(BM.getHeight()):
          [r,g,b]=BM.getPixel(x,y)
          BM.setPixel(x,y,[255-r,255-g,255-b])
    BM.update()
def spiegeln():
    for x in range(BM.getWidth()):
       for y in range(BM.getHeight()):
          BM.setPixel(BM.getWidth()-x-1,y,BM.getPixel(x,y))
    BM.update()
def unscharf():
    for x in range(1,BM.getWidth()-1):
       for y in range(1,BM.getHeight()-1):
           [r,g,b]=[0,0,0]
           for i in range(-1,2):
               for j in range(-1,2):
                   [rr,gg,bb]=BM.getPixel(x+i,y+j)
                   r+=rr
                   g+=gg
                   b+=bb
           BM.setPixel(x,y,[r/9,g/9,b/9])
    BM.update()
SWHBox()
SWButton(text="Negativ", command=negativ)
SWButton(text="spiegeln", command=spiegeln)
SWButton(text="unscharf", command=unscharf)


SWstart()


