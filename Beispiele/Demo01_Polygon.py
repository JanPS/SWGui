from SWGui import *
from random import randrange

SWLabel("Malprogramm")
b=600
h=400
BM=SWImage(dim=[b,h])

def zufallspunkt(): return [randrange(0,b),randrange(0,h)]
for i in range(3,10):
    BM.drawPolygon([zufallspunkt() for j in range(i)],
                    filled=True,
                    col=[randrange(0,255),randrange(0,255),randrange(0,255)])
SWstart()

