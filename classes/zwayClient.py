import logging;
import requests;
import time;

from classes.topic import Type;
from device import Device;

class ZwayClient:

  __PATH = "/ZAutomation/api/v1";
  
  __config = None;
  __mqttClient = None;
  __sid = None;
  __devices = {};
  __pollinterval = None;

  def __init__(self, config, mqttClient):
    self.__setConfig(config);
    self.__setMqttClient(mqttClient);
    self.__setDevices({});
    
  def __getConfig(self):
    return self.__config;
	
  def __setConfig(self, config):
    self.__config = config;
	
  def __getMqttClient(self):
    return self.__mqttClient;
	
  def __setMqttClient(self, mqttClient):
    self.__mqttClient = mqttClient;
	
  def __getSid(self):
    return self.__sid;
    
  def __setSid(self, sid):
    self.__sid = sid;
	
  def __getDevices(self):
	return self.__devices;
	
  def __setDevices(self, devices):
    self.__devices = devices;
	
  def __getPollinterval(self):
	return self.__pollinterval;
	
  def __setPollinterval(self, pollinterval):
    self.__pollinterval = pollinterval;
	
  def start(self):
    for topic in self.__getConfig().getMqtt().getTopics().values():
      if (self.__getPollinterval() == None):
        self.__setPollinterval(topic.getRefreshinterval());
      elif (topic.getRefreshinterval() < self.__getPollinterval()):
        self.__setPollinterval(topic.getRefreshinterval());
	  
    if (self.__getPollinterval() == None):
      self.__setPollinterval(60);
		
    if (self.__login()):
      firstRead = True;
      while True:
        self.__readDevices();
		
        if (firstRead):
          firstRead = False;
		  
          for topic in self.__getConfig().getMqtt().getTopics().values():
		    key = topic.getPath() + "/" + topic.getProperty();
			
		    if (key not in self.__getDevices()):
		      logging.error("topic \"" + topic.getPath() + "\" not found!");
	
  def __login(self):
    if (self.__getConfig().getZway().getUsername() != None and self.__getConfig().getZway().getPassword() != None):
	  
      url = self.__getUrl("login");

      try:
        response = requests.post(url, {"login": self.__getConfig().getZway().getUsername(), "password": self.__getConfig().getZway().getPassword()});
      except requests.exceptions.ConnectionError:
	    time.sleep(5);
	    logging.error("could not connect!");
	    return False;
	  
      if (response.status_code == 200):
          self.__setSid(response.json()['data']['sid']);
          logging.info("logged in to zwave api, got sid:" + self.__getSid());
          return True;
      else:
          self.__setSid(None);
          logging.error("could not login " + url + ": \n" + response.text);
          return False;
		  
  def writeDevice(self, topic, value):

    if (self.__getSid() != None):
	
      if (topic == "init" and value.lower() == "true"):
	    self.__setDevices({});
	    logging.warning("inited devices!");
	    return;

      temp = self.__getConfig().getMqtt().getTopicByTopic(topic);

      if (temp != None):
        url = self.__getUrl("devices/ZWayVDev_zway_" + temp.getId() + "/command/");
		
        if (temp.getType() == Type.INTEGER):
          value = int(value);
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
          logging.error("could not connect!");
          time.sleep(1);
          self.__login();
          self.writeDevice(topic, value);
          return;
		  
        if (response.status_code == 200):
          self.__publishDevice(temp, value, None, True);

          logging.info("did update device: " + url);
        elif (response.status_code == 403):
          time.sleep(1);
          self.__login();
          self.writeDevice(topic, value);
        else:
          logging.error("could not update device: " + url + "\n" + response.text);

  def __readDevices(self):
    if (self.__getSid() != None):
      url = self.__getUrl("devices");
	
      try:
        response = requests.get(url, headers={"ZWAYSession": self.__getSid()});
      except requests.exceptions.ConnectionError:
        logging.error("could not connect!");
        time.sleep(1);
        self.__login();
        return;
		
      if (response.status_code == 200):
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
                        if (now - self.__getDevices()[key].getUpdateTime() > topic.getRefreshinterval() * 100):
                          update = True;
                      else:
                        update = True;


                      if (update):

                        self.__publishDevice(topic, value, updateTime, False);
      else:
        logging.error("could not refresh devices " + url + ": \n" + response.text)
    else:
      self.api_devices = None
      logging.error("could not refresh devices " + url + ": \n" + response.text);
	  
    time.sleep(self.__getPollinterval());
	
  def __publishDevice(self, topic, value, updateTime, force):

    if (topic.getType() == Type.INTEGER):
      value = int(value);
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
						
    now = int(time.time() * 100);
						
    update = False;
	
    key = topic.getPath() + "/" + topic.getProperty();

    if (key in self.__getDevices()):
      device = self.__getDevices()[key];

      if (value != device.getValue()):
        if (updateTime == None or updateTime > device.getUpdateTime()):
          device.setUpdateTime(now);
          device.setValue(value);
          update = True;
        else:
          logging.warning("do not update device \"" + key + "\" from \"" + str(device.getValue()) + "\" to \"" + str(value) + "\" because updateTime is to old");
    else:
      device = Device(value, now);
      self.__getDevices()[key] = device;
      update = True;
						
    if (update):
      self.__getMqttClient().publish(topic.getPath(), str(device.getValue()));
	  
  def __getUrl(self, path):
    return "http://" + self.__getConfig().getZway().getHostname() + ":" + str(self.__getConfig().getZway().getPort()) + self.__PATH + "/" + path;