from thorpy.comm.discovery import discover_stages
from thorpy.message.motorcontrol import *

stages=list(discover_stages())

xmotor=stages[0] ; ymotor=stages[1]

object_methods = [method_name for method_name in dir(xmotor) if callable(getattr(xmotor, method_name))]

print(object_methods)

#xmotor.home() ; ymotor.home()

x=0 ; y=0

steps_per_mm = 34527.5


while True:
	control=input("do what:") #x=newCoord, x+=incrementBy, gx
	if "g" in control:
		print(x,y)
		xmotor.print_state()
		ymotor.print_state()
	if "x=" in control:
		print(xmotor.position)
		newCoord=int(control.split("=")[1])
		xmotor._port.send_message(MGMSG_MOT_MOVE_ABSOLUTE_long(xmotor._chan_ident, int(newCoord*steps_per_mm)))
	if "y=" in control:
		newCoord=int(control.split("=")[1])
		ymotor.position(newCoord)
