import re,binascii
from subprocess import Popen, PIPE
import xml.etree.ElementTree as et
from network import Cell


class Profile(object):
	"""docstring for Profile"""
	def __init__(self):
		self.name = None



	def find(self, profile_name, interface = None):
		command = ['netsh', 'wlan', 'show', 'profile', 'name={}'.format(profile_name)]
		if interface:
			command.append('interface='+interface)
		p = Popen(command, stdout=PIPE)
		(stdout, stderr) = p.communicate()
		if profile_name in stdout.decode():
			profile = Profile()
			profile.name = profile_name
			return profile
		else:
			return None



	def connect(self):
		profile_name = self.name
		command = ['netsh', 'wlan', 'connect', 'name={}'.format(profile_name)]
		p = Popen(command, stdout=PIPE)
		(stdout, stderr) = p.communicate()
		if "successfully" in stdout.decode():
			return "Connected"
		else:
			return None

			

	def add(self, cell, passkey = None):
		if passkey:
			filename = "wifi.xml"
		else:
			filename = "wifi_no_key.xml"
		tree = et.parse(filename)
		root = tree.getroot()
		root[0].text = cell.ssid
		hexa = binascii.hexlify(cell.ssid.encode()).upper()
		root[1][0][0].text = hexa.decode()
		root[1][0][1].text = cell.ssid
		if passkey:
			root[4][0][1][2].text = passkey

		tree.write(filename)
		command = ['netsh', 'wlan', 'add', 'profile', 'filename={}'.format(filename)]
		p = Popen(command, stdout=PIPE)
		(stdout, stderr) = p.communicate()
		if "added" in stdout.decode():
			return True
		else:
			return None




		

if __name__ == '__main__':
	profile = Profile()
	cell = Cell()
	cell.ssid = "binoy"
	out = profile.add(cell)
	print(out)