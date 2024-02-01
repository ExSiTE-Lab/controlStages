from thorpy.comm.discovery import discover_stages
#from thorpy.message.motorcontrol import *

stages=list(discover_stages())
xmotor=stages[0] ; ymotor=stages[1]

factor=1000 # to convert mm to um
mode="a"
while True:
	print("X:"+str(xmotor.position*factor)+", Y:"+str(ymotor.position*factor)+", mode="+mode)
	control=input("do what:") #"x=5" to set x to 5, "y-=4" to decrement y by 4, etc
	if "g" in control:
		xmotor.print_state()
		ymotor.print_state()
	if "q" in control:
		break
	if "r" in control:
		mode="r"
	if "a" in control:
		mode="a"
	if "," in control:
		control=control.split(",")
		distx,disty=control[:2]
		distx={True:"0",False:distx}[len(distx)==0]
		disty={True:"0",False:disty}[len(disty)==0]
		distx=float(distx)/factor ; disty=float(disty)/factor
		if mode=="a":
			if distx!=0:
				xmotor.setPosition(distx)
			if disty!=0:
				ymotor.setPosition(disty)
		if mode=="r":
			xmotor.changePosition(distx)
			ymotor.changePosition(disty)

	# pick which motor
	if "x" in control:
		mot=xmotor
	elif "y" in control:
		mot=ymotor
	else:
		continue
	# parse out distance, and absolute vs relative
	dist=float(control.split("=")[1])/factor
	if "-=" in control:
		dist=dist*-1
	if "+=" in control or "-=" in control:
		mot.changePosition(dist)
	else:
		mot.setPosition(dist)
