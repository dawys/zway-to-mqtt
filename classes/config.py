import sys;
import os;
import xml.etree.ElementTree as et;

from loggingConfig import LoggingConfig;
from mqttConfig import MqttConfig;
from zwayConfig import ZwayConfig;

class Config:
	__logger = None;
	__mqtt = None;
	__zway = None;

	def __init__(self):

		path = os.path.dirname(sys.argv[0]);

		# parse xml
		tree = et.parse(os.path.join (path, "config.xml"));
		
		root = tree.getroot();
		
		LoggingConfig(root);
		
		self.setMqtt(MqttConfig(root));
		self.setZway(ZwayConfig(root));
		
	def getLogger(self):
		return self.__logger;
		
	def setLogger(self, logger):
		self.__logger = logger;
		
	def getMqtt(self):
		return self.__mqtt;
		
	def setMqtt(self, mqtt):
		self.__mqtt = mqtt;
		
	def getZway(self):
		return self.__zway;
		
	def setZway(self, zway):
		self.__zway = zway;