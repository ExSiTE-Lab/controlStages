# USE THIS CODE TO CONTROL THORLABS' KB101 MOTOR CONTROLLERS, FROM PYTHON

import sys
from thorpy.comm.discovery import discover_stages
#from thorpy.message.motorcontrol import *


stages=list(discover_stages())
if len(stages)==0:
	print("No stages recognized: are you connected, and did you run as root?")
	sys.exit()
names=["X","Y","Z"]

factor=1000 # to convert mm to um
mode="a"
while True:
	ps=[n+":"+str(s.position*factor) for n,s in zip(names,stages)]
	print(", ".join(ps)+", mode="+mode) 		# "X:x.xxx, Y:y.yyy, Z:z.zzz, mode=a"
	control=input("do what:")
	if "g" in control:				# "g" to "get" info for all stages
		for motor in stages:
			motor.print_state()
	if "q" in control:				# "q" to "quit"
		break
	if "r" in control:				# "r" set mode to "relative"
		mode="r"
	if "a" in control:				# "a" set  mode to "absolute"
		mode="a"
	if "," in control:				# 1,2,3 to change or set x to/by 1, y to/by 2
		control=control.split(",")
		for i,d in enumerate(control):		# for each value
			if len(d)==0:			# skip empty
				continue
			d=float(d)/factor		# convert mm to um (for example)
			if mode=="a":			# "absolute" mode -> set position
				stages[i].setPosition(d)
			elif mode=="r":			# "relative" mode -> change position
				stages[i].changePosition(d)
