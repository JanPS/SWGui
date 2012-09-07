from SWGui import *
from random import *

SWLabel("GrafikObjekte")
[w,h]=[400,400]
G=SWGraphics(w,h)

def klick(obj,event): 
    obj.hide()
    
objekte=[]
for i in range(10):
    kreis=G.addCircle(randrange(w),randrange(h),10,color="red",fillcolor="red")
    objekte.append(kreis)
    kreis.setMousePressCommand(klick)
    
SWstart()
  