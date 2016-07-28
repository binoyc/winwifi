import re
from subprocess import Popen, PIPE


class Interface(object):
	"""docstring for Interface"""
	def __init__(self):
		self.name = None
		self.description = None
		self.mac = None
		self.state = None
		self.ssid = None
		self.profile = None


	def all(self):
		p = Popen(['netsh', 'wlan', 'show', 'interfaces'], stdout=PIPE)
		(stdout, stderr) = p.communicate()
		return to_object(parse(stdout))

	def disconnect(self):
		p = Popen(['netsh', 'wlan', 'disconnect'], stdout=PIPE)
		(stdout, stderr) = p.communicate()
		if "successfully" in stdout.decode() or "" in stdout.decode():
			return True
		else:
			return None


def parse(stdout):
	interfaces = []
	stdout = stdout.decode().split('\r\n')
	#print no of interfaces
	print(re.sub('[^0-9]','', stdout[1]))

	for std in stdout:
		std = std.split(': ', 1)[-1]
		#std = std.split(': ', 1)[0].replace('    ', '')
		if std:
			interfaces.append(std);
	#print(stdout)
	#print(interfaces)
	return interfaces
		


def to_object(output):
	interface = Interface()
	interface.name = output[0]	
	interface.description = output[1]
	interface.mac = output[3]	
	state = output[4]
	interface.state = state
	if state == "connected":
		interface.ssid = output[5]
		interface.profile = output[16]
	return interface



if __name__ == '__main__':
	interface = Interface()
	out = interface.disconnect()
	print(out)
	
		
				
