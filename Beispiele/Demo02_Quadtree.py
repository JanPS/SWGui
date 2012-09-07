from SWGui import *

SWsetWindowSize(1000,500)
SWLabel("Quadtrees")
SWHBox()
BM=SWGraphics(file="img/blitzGrau.jpg")
[w,h]=[BM.getWidth(), BM.getHeight()]
BM2=SWGraphics(dim=[w,h])
BM2.drawRect(0,0,w,h,"yellow",filled=True)
BM.update()
BM2.update()
TheMainWin.updateGeometry()

print "Bild geladen", [w,h]

class QuadTree:
    def __init__(self,bitmap,x0,x1,y0,y1): # Info aus angegebenem bereich
        self.coords=[x0,y0,x1-x0,y1-y0]
        if x1-x0==0 or y1-y0==0:
            self.wert=bitmap.getPixelGray(x0,y0)
            self.istBlatt=True
            return
        summe=0
        maximum=0
        minimum=255
        for x in range(x0,x1):
            for y in range(y0,y1):
                w=bitmap.getPixelGray(x,y)
                summe+=w
                if w>maximum: maximum=w
                if w<minimum: minimum=w
        self.wert=int(summe/float((x1-x0)*(y1-y0)))
        self.istBlatt= maximum-minimum<20
        if not(self.istBlatt):
            b2=(x1-x0)/2
            h2=(y1-y0)/2
            self.LU=QuadTree(bitmap,x0,x0+b2,y0+h2,y1)
            self.LO=QuadTree(bitmap,x0,x0+b2,y0,y0+h2)
            self.RU=QuadTree(bitmap,x0+b2,x1,y0+h2,y1)
            self.RO=QuadTree(bitmap,x0+b2,x1,y0,y0+h2)
    def draw(self,bitmap):
        if self.istBlatt:
            bitmap.drawRect(self.coords[0],self.coords[1],
                        self.coords[2],self.coords[3],
                        col=self.wert,filled=True)
        else:
            self.LU.draw(bitmap)
            self.LO.draw(bitmap)
            self.RU.draw(bitmap)
            self.RO.draw(bitmap)
    def bericht(self,level):
        if level==0 or self.istBlatt:
            return self.wert
        return [self.LO.bericht(level-1),self.RO.bericht(level-1),
                self.LU.bericht(level-1),self.RU.bericht(level-1)]
    def blattZahl(self):
        if self.istBlatt: return 1
        else: return self.LU.blattZahl()+self.LO.blattZahl()+self.RO.blattZahl()+self.RU.blattZahl()
    
        
qt=QuadTree(BM,0,w,0,h)
qt.draw(BM2)
BM2.update()
print qt.bericht(4)
print qt.blattZahl(), " Blaetter bei ",w*h," Pixel"

SWstart()


