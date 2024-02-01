# USE THIS CODE TO CONTROL THORLABS' KB101 MOTOR CONTROLLERS, FROM PYTHON
# re-written to use tpchuckles' ThorlabsKinesis > pylablib instead of thorpy (which does not work on Windows)

import sys
import tkinter as tk ; import numpy as np
#from thorpy.comm.discovery import discover_stages
#from thorpy.message.motorcontrol import *
from ThorlabsKinesis import *

stages=findStages()

if len(stages)==0:
	print("No stages recognized: are you connected, and did you run as root?") # nope. don't run as root. https://stackoverflow.com/questions/53125118/why-is-python-pyusb-usb-core-access-denied-due-to-permissions-and-why-wont-the
	sys.exit()
names=["X","Y","Z"]

factor=2.9151/100000*1e3 # 2.9151 mm / 100000 steps. # to convert mm to um
mode="a"

window=tk.Tk() ; window.title("controlStages")
frames=[]
for i in range(4):									# "refresh / goto" buttons
	frame=tk.Frame(master=window,highlightbackground="black",highlightthickness=1)	# curX,Y,Z fields
	frame.grid(row=i,column=0)							# "inc/dec" buttons (3x4)
	frames.append(frame)								# increment fields

#fields={"curX":str(stages[0].position*factor), "curY":str(stages[1].position*factor), "curZ":str(stages[2].position*factor),
fields={"curX (μm)":"N/A", "curY (μm)":"N/A", "curZ (μm)":"N/A",
	"incSmall (μm)":10, "incLarge (μm)":100}

counters=[0,0,0,0]
for k in fields.keys():
	i={True:1,False:3}["cur" in k] 			# which frame, which column counter
	lb=tk.Label(master=frames[i],text=k)		# create a label, text is just field name
	lb.grid(row=0,column=counters[i])		# row 0 is the label, row 1, below it, is each field
	field=tk.Entry(master=frames[i],width=10)
	val=fields[k]					# current val, taken from the dict
	field.insert(0,val)				# inserted to the field
	fields[k]=field					# field is saved off in the dict (replacing the current val)
	field.grid(row=1,column=counters[i])
	counters[i]+=1					# increment column counter

def refresh(event):
	for i,k in enumerate(["curX (μm)","curY (μm)","curZ (μm)"]):
		if i>=len(stages):
			continue
		v=np.round(stages[i].get_position()*factor,2)
		fields[k].delete(0,tk.END)
		fields[k].insert(0,str(v))

def gotoXYZ(event):
	for i,k in enumerate(["curX (μm)","curY (μm)","curZ (μm)"]):
		if i>=len(stages):
			continue
		v=float(fields[k].get())
		stages[i].move_to(v/factor)

def chg(whichStage,bigOrSmall,plusOrMinus=1):
	by={"big":float(fields["incLarge (μm)"].get()), "small":float(fields["incSmall (μm)"].get())}[bigOrSmall]
	print(by)
	if whichStage>=len(stages):
		return
	stages[whichStage].move_by(by*plusOrMinus/factor)

def mmX(event):
	chg(0,"big",-1)
def mX(event):
	chg(0,"small",-1)
def pX(event):
	chg(0,"small",1)
def ppX(event):
	chg(0,"big",1)
def mmY(event):
	chg(1,"big",-1)
def mY(event):
	chg(1,"small",-1)
def pY(event):
	chg(1,"small",1)
def ppY(event):
	chg(1,"big",1)
def mmZ(event):
	chg(2,"big",-1)
def mZ(event):
	chg(2,"small",-1)
def pZ(event):
	chg(2,"small",1)
def ppZ(event):
	chg(2,"big",1)

def focusOnSample(event):
	stages[2].move_by(-25/factor)
def focusLaser(event):
	stages[2].move_by(25/factor)

buttons={"refresh":refresh, "gotoXYZ":gotoXYZ,
	"--x":mmX, "-x":mX, "+x":pX, "++x":ppX,
	"--y":mmY, "-y":mY, "+y":pY, "++y":ppY, 
	"--z":mmZ, "-z":mZ, "+z":pZ, "++z":ppZ,
	"focSample":focusOnSample , "focLas":focusLaser }

for k in buttons.keys():
	i={True:2,False:0}[("+" in k) or ("-" in k)] 	# which frame, which column counter
	bu=tk.Button(master=frames[i],text=k)		# text on the button is just the dict key
	bu.bind("<Button-1>", buttons[k])		# "<Button-1>" is for left click
	r=0
	if "+" in k or "-" in k:
		r=["x","y","z"].index(k[-1])		# x,y,z on different rows
	bu.grid(row=r,column=counters[i]%4)
	counters[i]+=1

window.bind('<Up>',mmY)
window.bind('<Down>',ppY)
window.bind('<Left>',mmX)
window.bind('<Right>',ppX)
window.bind('<Control-Up>',pZ)
window.bind('<Control-Down>',mZ)




window.mainloop()
