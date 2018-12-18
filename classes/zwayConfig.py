import logging;
from croniter import croniter;
from classes.job import Job;
import time;

class ZwayConfig:

	__hostname = "localhost";	
	__port = 8083;
	__timeout = 60;
	__username = None;
	__password = None;
	__jobs = None;
	
	def __init__(self, root):

		self.setJobs({});

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

		logging.info("cron jobs configured:");
		jobs = root.findall("zway/cron/job");
		if (jobs != None):
			now = time.time();
		
			for entry in jobs:
				attributes = entry.attrib;

				if (entry.text != None and len(entry.text.strip()) > 0 and "id" in attributes and attributes["id"] != None and len(attributes["id"].strip()) > 0):

					scheduler = croniter(entry.text.strip(), now);
					job = Job(scheduler, int(scheduler.get_next() * 100));
					
					self.getJobs()[attributes["id"].strip()] = job;
					logging.info("cron job for device with id \"" + attributes["id"].strip() + "\" all " + entry.text.strip() + " and next execution " + time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(job.getNextTime() / 100)));
			
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

	def getJobs(self):
		return self.__jobs;

	def setJobs(self, jobs):
		self.__jobs = jobs;
