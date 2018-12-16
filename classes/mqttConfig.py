import logging;

from classes.topic import *;

class MqttConfig:

	__hostname = "localhost";	
	__port = 1883;
	__timeout = 60;
	__username = None;
	__password = None;
	__qosPublish = 0;
	__qosSubscribe = 0;
	__retain = 0;
	__topicPrefix = None;
	__refreshInterval = 60;
	__topics = None;
	__deviceMapping = None;
	
	def __init__(self, root):
		self.setTopics({});
		self.__setDeviceMapping({});
	
		hostname = root.find("mqtt/hostname");
		if (hostname != None and hostname.text.strip() != ""):
			self.setHostname(hostname.text.strip());
			
		port = root.find("mqtt/port");
		if (port != None and port.text.strip() != ""):
			self.setPort(int(port.text.strip()));
			
		timeout = root.find("mqtt/timeout");
		if (timeout != None and timeout.text.strip() != ""):
			self.setTimeout(int(timeout.text.strip()));
			
		username = root.find("mqtt/username");
		if (username != None and username.text.strip() != ""):
			self.setUsername(username.text.strip());
			
		password = root.find("mqtt/password");
		if (password != None and password.text.strip() != ""):
			self.setPassword(password.text.strip());
		
		qosPublish = root.find("mqtt/qosPublish");
		if (qosPublish != None and qosPublish.text.strip() != ""):
			self.setQosPublish(int(qosPublish.text.strip()));
		
		qosSubscribe = root.find("mqtt/qosSubscribe");
		if (qosSubscribe != None and qosSubscribe.text.strip() != ""):
			self.setQosSubscribe(int(qosSubscribe.text.strip()));
		
		retain = root.find("mqtt/retain");
		if (retain != None and retain.text.strip() != ""):
			self.setRetain(int(retain.text.strip()));
		
		topicPrefix = root.find("mqtt/topicPrefix");
		if (topicPrefix != None and topicPrefix.text.strip() != ""):
			self.setTopicPrefix(topicPrefix.text.strip());
		
		refreshInterval = root.find("mqtt/refreshInterval");
		if (refreshInterval != None and refreshInterval.text.strip() != ""):
			self.setRefreshInterval(int(refreshInterval.text.strip()));		

		logging.info("Topics configured:");
		topics = root.findall("mqtt/topics/topic");
		if (topics != None):
			for entry in topics:
				attributes = entry.attrib;
		
				if (entry.text != None and entry.text.strip() != "" and "id" in attributes and "type" in attributes and attributes["id"] != None and len(attributes["id"].strip()) > 0 and attributes["type"] != None and len(attributes["type"].strip()) > 0):
			
					property = None;
					if ("property" in attributes and attributes["property"] != None and len(attributes["property"].strip()) > 0):
						property = attributes["property"].strip();
			
					refreshInterval = self.getRefreshInterval();
					if ("refreshInterval" in attributes and attributes["refreshInterval"] != None and len(attributes["refreshInterval"].strip()) > 0):
						refreshInterval = int(attributes["refreshInterval"].strip());
			
					topic = Topic(attributes["id"].strip(), property, attributes["type"].strip(), entry.text.strip(), refreshInterval);
			
					if ("invert" in attributes and attributes["invert"] != None and len(attributes["invert"].strip()) > 0 and attributes["invert"].strip().lower() == "true"):
						topic.setInvert(True);
			
					if (topic.getId() in self.__getDeviceMapping()):
						if (topic.getProperty() == None):
							topic.setProperty(str(len(self.__getDeviceMapping()[topic.getId()]) + 1));
						self.__getDeviceMapping()[topic.getId()][topic.getProperty()] = topic.getPath();
					else:
						if (topic.getProperty() == None):
							topic.setProperty("1");
						self.__getDeviceMapping()[topic.getId()] = {topic.getProperty(): topic.getPath()};
			
					self.getTopics()[topic.getPath()] = topic;
			
					logging.info(topic.log());
		
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

	def getQosPublish(self):
		return self.__qosPublish;
		
	def setQosPublish(self, qosPublish):
		self.__qosPublish = qosPublish;
	
	def getQosSubscribe(self):
		return self.__qosSubscribe;
		
	def setQosSubscribe(self, qosSubscribe):
		self.__qosSubscribe = qosSubscribe;
	
	def getRetain(self):
		return self.__retain;
		
	def setRetain(self, retain):
		self.__retain = retain;
	
	def getTopicPrefix(self):
		return self.__topicPrefix;
	
	def setTopicPrefix(self, topicPrefix):
		self.__topicPrefix = topicPrefix;
	
	def getRefreshInterval(self):
		return self.__refreshInterval;
	
	def setRefreshInterval(self, refreshInterval):
		self.__refreshInterval = refreshInterval;
	
	def getTopics(self):
		return self.__topics;
	
	def setTopics(self, topics):
		self.__topics = topics;
	
	def __getDeviceMapping(self):
		return self.__deviceMapping;
	
	def __setDeviceMapping(self, deviceMapping):
		self.__deviceMapping = deviceMapping;
	
	def getTopicByTopic(self, topic):
		if (topic in self.getTopics()):
			return self.getTopics()[topic];
		
		return None;
	
	def getTopicsByDevice(self, device):
	
		result = [];
		if (device in self.__getDeviceMapping()):
			topics = self.__getDeviceMapping()[device];
		
			if (topics != None):
				for topic in topics.values():
					temp = self.getTopicByTopic(topic);

					if (temp != None):
						result.append(temp);

		return result;
	