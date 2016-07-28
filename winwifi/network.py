import re
from subprocess import Popen, PIPE

class Cell(object):
	"""docstring for Cell"""
	def __init__(self):
		self.ssid = None


	def all(self, interface = None):
		command = ['netsh', 'wlan', 'show', 'networks', 'mode=bssid']
		if interface:
			command.append('interface='+interface)
		p = Popen(command, stdout=PIPE)
		(stdout, stderr) = p.communicate()
		#print(stdout)
		return to_cell(stdout)


def to_cell(stdout):
	cells = []
	cell_strings = stdout.decode().split('\r\n\r\n')
	for cell_string in cell_strings:
		if "SSID" in cell_string:
			cell = normalize(cell_string)
			cells.append(cell)
	return cells


def normalize(cell_string):
	cell_attr = parse(cell_string)
	cell = Cell()
	cell.ssid = cell_attr[0]
	cell.auth = cell_attr[2]
	cell.encryption = cell_attr[3]
	cell.address = cell_attr[4]
	cell.signal = cell_attr[5]
	cell.channel = cell_attr[7]
	return cell


def parse(cell_string):
	cell_attr = []
	attr = cell_string.split('\r\n')
	for s in attr:
		s = s.split(': ',1)[-1]
		cell_attr.append(s)
	return cell_attr


		

if __name__ == '__main__':
	cell = Cell()
	out = cell.all()