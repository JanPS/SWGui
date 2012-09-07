# Springene Baelle ala Modrow mit MySWGui.py
import time
from SWGui import *
from math import *

SWLabel(text="Test-Programm")
Frame1=SWHBox()
bSchneller=SWButton(container=Frame1,text="schneller")
bLangsamer=SWButton(container=Frame1,text="langsamer")

Feld=SWGraphics(width=400,height=400)

SWshow()

ball=Feld.addCircleW(-5,5,1.0)
ball.setColor('red')
ball.setFillColor('yellow')
ball.vx=0.3
ball.vy=0.1

def schneller():
    ball.vx=ball.vx*2
    ball.vy=ball.vy*2
def langsamer():
    ball.vx=ball.vx/2.0
    ball.vy=ball.vy/2.0
bLangsamer.setCommand(langsamer)
bSchneller.setCommand(schneller)

dt=0.05 # Zeitschritt der Simulation
g=-9.0 # "Erd"beschelunigung
[breite,hoehe]=Feld.getDim()

while True:
    ball.vy=ball.vy+dt*g
    ballX=ball.getXW()
    ballY=ball.getYW()
    if ballY<-10:  ball.vy=abs(ball.vy)
    if ballY>10:  ball.vy=-abs(ball.vy)
    if ballX<-10:  ball.vy=abs(ball.vx)
    if ballX>10:  ball.vy=-abs(ball.vx)
    ball.setCenterW(ballX+ball.vx*dt, ballY+ball.vy*dt)
    time.sleep(dt)
    SWinteract()





