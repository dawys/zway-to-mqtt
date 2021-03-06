import logging;
import requests;
import time;
import math;
from threading import Thread;

from classes.topic import Type;
from device import Device;

class ZwayClient:

	__PATH = "/ZAutomation/api/v1";
	
	__stop = False;
	__config = None;
	__sid = None;	
	__connected = False;
	__mqttClient = None;
	__devices = {};
	__pollInterval = None;
	__updateDevices = None;

	def __init__(self, config, mqttClient):
		self.__setConfig(config);
		self.__setMqttClient(mqttClient);
		self.__setDevices({});
		self.__setStop(False);
		self.__setConnected(False);
		
	def __getStop(self):
		return self.__stop;
	
	def __setStop(self, stop):
		self.__stop = stop;		
		
	def __getConfig(self):
		return self.__config;
	
	def __setConfig(self, config):
		self.__config = config;
	
	def __getSid(self):
		return self.__sid;
		
	def __setSid(self, sid):
		self.__sid = sid;	
	
	def __getConnected(self):
		return self.__connected;
	
	def __setConnected(self, connected):
		self.__connected = connected;	
	
	def __getMqttClient(self):
		return self.__mqttClient;
	
	def __setMqttClient(self, mqttClient):
		self.__mqttClient = mqttClient;
	
	def __getDevices(self):
		return self.__devices;
	
	def __setDevices(self, devices):
		self.__devices = devices;
	
	def __getPollInterval(self):
		return self.__pollInterval;
	
	def __setPollInterval(self, pollInterval):
		self.__pollInterval = pollInterval;
	
	def start(self):
		for topic in self.__getConfig().getMqtt().getTopics().values():
			if (self.__getPollInterval() == None):
				self.__setPollInterval(topic.getRefreshInterval());
			elif (topic.getRefreshInterval() < self.__getPollInterval()):
				self.__setPollInterval(topic.getRefreshInterval());
		
		if (self.__getPollInterval() == None):
			self.__setPollInterval(60);
			
		if (self.__getConfig().getZway().getUsername() != None and self.__getConfig().getZway().getPassword() != None):
			
			thread1 = Thread(target=self.__connect, args=[]);
			thread2 = Thread(target=self.__readDevices, args=[]);
			thread3 = Thread(target=self.__cronJobs, args=[]);
			
			thread1.start();
			thread2.start();
			thread3.start();
			
			try:
				while True:
					time.sleep(0.1);
			except (KeyboardInterrupt, SystemExit):
				self.__setStop(True);
				thread1.join();
				thread2.join();
				thread3.join();

	def __connect(self):
		
		while True:
		
			if (not self.__getConnected()):
		
				url = self.__getUrl("login");
				
				response = None;

				try:
					response = requests.post(url, {"login": self.__getConfig().getZway().getUsername(), "password": self.__getConfig().getZway().getPassword()});
				except requests.exceptions.ConnectionError:
					logging.error("could not connect!");
					self.__setConnected(False);
			
				if (response != None):
					if (response.status_code == 200):
						self.__setSid(response.json()['data']['sid']);
						logging.info("logged in to zwave api, got sid:" + self.__getSid());
						self.__setConnected(True);
					else:
						self.__setSid(None);
						logging.error("could not login " + url + ": \n" + response.text);
						self.__setConnected(False);
				else:
					logging.error("could not login " + url);
					self.__setConnected(False);
				
			for i in range(5 * 10):
				time.sleep(0.1);
				if (self.__getStop()):
					return;
			
	def writeDevice(self, topic, value):
	
		if (self.__getStop()):
			return;	

		if (self.__getConnected() and self.__getSid() != None):
	
			if (topic == "init" and value.lower() == "true"):
				self.__setDevices({});
				logging.warning("inited devices!");
				return;

			temp = self.__getConfig().getMqtt().getTopicByTopic(topic);

			if (temp != None):
				url = self.__getUrl("devices/ZWayVDev_zway_" + temp.getId() + "/command/");
		
				if (temp.getType() == Type.INTEGER):
					value = int(value);
				elif (temp.getType() == Type.LONG):
					value = long(value);					
				elif (temp.getType() == Type.FLOAT):
					value = float(value);
				elif (temp.getType() == Type.ON_OFF):
						if (value == "0" or value.lower() == "off"):
							value = "off";
						else:
							value = "on";
				
				if (temp.getType() == Type.ON_OFF and temp.getInvert()):
					if (value == "255"):
						value = 0;
					elif (value == "0"):
						value = 255;

				if (value == "on" or value == "off"):
					url += str(value);
				else:
					url += "exact?level=" + str(value);
		
				try:
					response = requests.get(url, headers={"ZWAYSession": self.__getSid()})
				except requests.exceptions.ConnectionError:
					logging.error("could not connect for wrting device");
					self.__setConnected(False);
					return;
			
				if (response.status_code == 200):
					self.__publishDevice(temp, value, None, True);

					logging.info("did update device: " + url);
				elif (response.status_code == 403):
					self.__setConnected(False);
					return;
				else:
					logging.error("could not update device: " + url + "\n" + response.text);

	def __readDevices(self):
	
		firstRead = True;
	
		while True:	
			if (self.__getConnected() and self.__getSid() != None):
			
				url = self.__getUrl("devices");
				
				response = None;
		
				try:
					response = requests.get(url, headers={"ZWAYSession": self.__getSid()});
				except requests.exceptions.ConnectionError:
					logging.error("could not connect for reading devices");
					self.__setConnected(False);
					sleep(5);
			
				if (response != None and response.status_code == 200):
				
					json = response.json();

					if ("data" in json):
						data = json["data"];
				
						if ("devices" in data):
							for device in data["devices"]:
								if ("id" in device and "metrics" in device and "deviceType" in device):
					
									metrics = device["metrics"];
					
									if ("level" in metrics): 
					
										value = metrics["level"];
					
										deviceType = device["deviceType"];				
										updateTime = long(device["updateTime"]) * 100;
										id = device["id"].replace("ZWayVDev_zway_", "");
						
										topics = self.__getConfig().getMqtt().getTopicsByDevice(id);

										if (len(topics) > 0):
											id = device["id"].replace("ZWayVDev_zway_", "");
						
											for topic in topics:
						
												key = topic.getPath() + "/" + topic.getProperty();
							
												now = int(time.time() * 100);
						
												update = False;
												if (key in self.__getDevices()):
													if (now - self.__getDevices()[key].getRefreshTime() > topic.getRefreshInterval() * 100):
														update = True;
												else:
													update = True;

												if (update):
													self.__publishDevice(topic, value, updateTime, False);
					else:
						logging.error("could not refresh devices " + url + ": \n" + response.text)
				else:
					self.api_devices = None;
					logging.error("could not refresh devices " + url + ": \n" + response.text);
				
				# check for missing topics
			
				if (firstRead):
					firstRead = False;
				
					for topic in self.__getConfig().getMqtt().getTopics().values():
						key = topic.getPath() + "/" + topic.getProperty();
				
						if (key not in self.__getDevices()):
							logging.error("topic \"" + topic.getPath() + "\" not found!");

			for i in range(self.__getPollInterval() * 10):
				time.sleep(0.1);
				if (self.__getStop()):
					return;

	
	def __publishDevice(self, topic, value, updateTime, force):

		if (topic.getType() == Type.INTEGER):
			value = int(value);
		elif (topic.getType() == Type.LONG):
			value = long(value);			
		elif (topic.getType() == Type.FLOAT):
			value = float(value);
		elif (topic.getType() == Type.ON_OFF):
			if (isinstance(value, int)):
				if (int(value) == 0):
					value = "OFF";
				else:
					value = "ON";
			else:
				if (value == "on"):
					value = "ON";
				elif (value == "off"):
					value = "OFF";
								
		if (topic.getType() == Type.ON_OFF and topic.getInvert()):
			if (value == "ON"):
				value = "OFF";
			elif (value == "OFF"):
				value = "ON";
						
		refreshTime = int(time.time() * 100);
						
		update = False;
	
		key = topic.getPath() + "/" + topic.getProperty();

		if (key in self.__getDevices()):
			device = self.__getDevices()[key];

			if (value != device.getValue()):
				if (updateTime == None or device.getUpdateTime() == None or updateTime > device.getUpdateTime()):
					if (updateTime == None):
						device.setUpdateTime(refreshTime);
					else:
						device.setUpdateTime(updateTime);
					device.setRefreshTime(refreshTime);
					device.setValue(value);
					update = True;
				else:
					logging.warning("do not update device \"" + key + "\" from \"" + str(device.getValue()) + "\" to \"" + str(value) + "\" because updateTime is to old");
		else:
			device = Device(value, updateTime, refreshTime);
			self.__getDevices()[key] = device;
			update = True;
						
		if (update):
			self.__getMqttClient().publish(topic.getPath(), str(device.getValue()));

	def __cronJobs(self):

		if (self.__getConfig().getZway().getJobs() != None and len(self.__getConfig().getZway().getJobs()) > 0):

			while True:
			
				now = (time.time() * 100);			

				for id in self.__getConfig().getZway().getJobs().keys():

					job = self.__getConfig().getZway().getJobs()[id];
					
					if (now >= job.getNextTime()):

						job.setNextTime((job.getScheduler().get_next() * 100));
		
						for topic in self.__getConfig().getMqtt().getTopics().values():	

							update = False;
							if (id[-1] == "*"):
								if (topic.getId()[:len(id) - 1] == id[:-1]):
									update = True;
							elif (topic.getId() == id):
								update = True;

							if (update):
								if (self.__getConnected() and self.__getSid() != None):
								
									logging.info("update device with id \"" + topic.getId() + "\"");
									url = self.__getUrl("devices/ZWayVDev_zway_" + topic.getId() + "/command/update");
									
									response = None;

									try:
										response = requests.get(url, headers={"ZWAYSession": self.__getSid()})
									except requests.exceptions.ConnectionError:
										logging.error("could not connect for updating devices");
										self.__setConnected(False);
								
									if (response == None or response.status_code == 403):
										self.__setConnected(False);
									elif (response.status_code != 200):
										logging.error("could not update device: " + url + "\n" + response.text);
										
										
				nextTime = None;

				for job in self.__getConfig().getZway().getJobs().values():
					if (nextTime == None):
						nextTime = job.getNextTime();
					elif (job.getNextTime() < nextTime):
						nextTime = job.getNextTime();
						
				logging.info("next scheduled " + time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(nextTime / 100)));

				nextInterval = int(math.ceil((nextTime - now) / 100));
				
				if (nextInterval <= 0):
					logging.error("next scheduled in " + str(nextInterval) + " seconds. Abort now");
					return;

				for i in range(nextInterval * 10):
					time.sleep(0.1);
					if (self.__getStop()):
						return;

		
	def __getUrl(self, path):
		return "http://" + self.__getConfig().getZway().getHostname() + ":" + str(self.__getConfig().getZway().getPort()) + self.__PATH + "/" + path;