from thorpy.comm.discovery import discover_stages
from thorpy.message.motorcontrol import *

stages=list(discover_stages())

xmotor=stages[0] ; ymotor=stages[1]

object_methods = [method_name for method_name in dir(xmotor) if callable(getattr(xmotor, method_name))]

print(object_methods)

#xmotor.home() ; ymotor.home()

x=0 ; y=0

def moveAbsolute(motorObj,newPos):
	steps_per_mm = 34527.5
	motorObj._port.send_message(MGMSG_MOT_MOVE_ABSOLUTE_long(motorObj._chan_ident, int(newPos*steps_per_mm)))

def moveRelative2(motorObj,moveBy):
	curLoc=motorObj.position
	newPos=curLoc+moveBy
	moveAbsolute(motorObj,newPos)

def moveRelative(motorObj,moveBy):
	steps_per_mm = 34527.5
	motorObj._port.send_message(MGMSG_MOT_MOVE_RELATIVE_long(motorObj._chan_ident, int(moveBy*steps_per_mm)))


while True:
	control=input("do what:") #x=newCoord, x+=incrementBy, gx
	if "g" in control:
		print(x,y)
		xmotor.print_state()
		ymotor.print_state()
	if "q" in control:
		break
	if "x" in control:
		mot=xmotor
	elif "y" in control:
		mot=ymotor
	else:
		continue
	dist=float(control.split("=")[1])
	if "-=" in control:
		dist=dist*-1
	if "+=" in control or "-=" in control:
		moveRelative(mot,dist)
	else:
		moveAbsolute(mot,dist)
