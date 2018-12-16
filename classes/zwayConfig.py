import logging;

class ZwayConfig:

	__hostname = "localhost";	
	__port = 8083;
	__timeout = 60;
	__username = None;
	__password = None;
	__updateDevices = None;
	
	def __init__(self, root):

		self.setUpdateDevices({});

		hostname = root.find("zway/hostname");
		if (hostname != None and hostname.text.strip() != ""):
			self.setHostname(hostname.text.strip());
			
		port = root.find("zway/port");
		if (port != None and port.text.strip() != ""):
			self.setPort(int(port.text.strip()));
		
		username = root.find("zway/username");
		if (username != None and username.text.strip() != ""):
			self.setUsername(username.text.strip());
			
		username = root.find("zway/username");
		if (username != None and username.text.strip() != ""):
			self.setUsername(username.text.strip());
			
		password = root.find("zway/password");
		if (password != None and password.text.strip() != ""):
			self.setPassword(password.text.strip());

		logging.info("Update devices configured:");
		devices = root.findall("zway/update/device");
		if (devices != None):
			for entry in devices:
				attributes = entry.attrib;

				if (entry.text != None and len(entry.text.strip()) > 0 and "id" in attributes and attributes["id"] != None and len(attributes["id"].strip()) > 0):

					value = entry.text.strip();

					time = None;
					if (value[-1] == "s"):
						time = long(value[:-1]);
					elif (value[-1] == "m"):
						time = long(value[:-1]) * 60;
					elif (value[-1] == "h"):
						time = long(value[:-1]) * 60 * 60;
					elif (value[-1] == "d"):
						time = long(value[:-1]) * 60 * 60 * 24;
					else:
						time = long(value);

					self.getUpdateDevices()[attributes["id"].strip()] = time;
			
					logging.info("update node " + attributes["id"].strip() + " all " +str(time) + " seconds");
			
	def getHostname(self):
		return self.__hostname;

	def setHostname(self, hostname):
		self.__hostname = hostname;

	def getPort(self):
		return self.__port;

	def setPort(self, port):
		self.__port = port;

	def getTimeout(self):
		return self.__timeout;

	def setTimeout(self, timeout):
		self.__timeout = timeout;
		
	def getUsername(self):
		return self.__username;
		
	def setUsername(self, username):
		self.__username = username;
		
	def getPassword(self):
		return self.__password;
		
	def setPassword(self, password):
		self.__password = password;

	def getUpdateDevices(self):
		return self.__updateDevices;

	def setUpdateDevices(self, updateDevices):
		self.__updateDevices = updateDevices;
