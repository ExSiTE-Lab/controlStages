def findStages():
	import platform
	from pylablib.devices import Thorlabs
	if platform.system() == 'Linux':
		# lifted STRAIGHT from github's UniNE-CHYN/thorpy-tp/thorpy/comm/discovery.py
		from serial.tools.list_ports import comports
		serial_ports = [(x[0], x[1], dict(y.split('=', 1) for y in x[2].split(' ') if '=' in y)) for x in comports()]
		print(serial_ports)
		devices = [ ] 
		for sp in serial_ports:
			# lifted STRAIGHT from https://github.com/AlexShkarin/pyLabLib/issues/34
			conn = {"port":sp[0],"baudrate":115200,"rtscts":True}
			dev=Thorlabs.KinesisMotor(("serial",conn))
			devices.append(dev)
		return devices
	else:
		options = Thorlabs.list_kinesis_devices()
		devices = [ ]
		for opt in options:
			dev=Thorlabs.KinesisMotor(opt[0])
			devices.append(dev)
		return devices




#devs = findStages()
#import time

#for dev in devs:
#	print(id(dev))
#	dev.move_to(10000)
#	time.sleep(1)
#	dev.move_to(0)
#	time.sleep(1)
	#dev.setPosition(10000)
	#dev.setPosition(0)

#print(dir(dev))