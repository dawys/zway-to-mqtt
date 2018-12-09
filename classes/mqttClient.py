import logging;
import traceback;
import socket;
import time;

import paho.mqtt.client as mqtt;

class MqttClient:

  __config = None;
  __client = None;
  __connected = False;
  __subscriberMethod = None;

  def __init__(self, config):
    self.__setConfig(config);
    self.connect();

  def __getConfig(self):
    return self.__config;
	
  def __setConfig(self, config):
    self.__config = config;
	
  def __getClient(self):
    return self.__client;
	
  def __setClient(self, client):
    self.__client = client;	
	
  def __getConnected(self):
    return self.__connected;
	
  def __getSubscriberMethod(self):
     return self.__subscriberMethod;
	 
  def __setSubscriberMethod(self, subscriberMethod):
    self.__subscriberMethod = subscriberMethod;
	
  def connect(self):
    self.__setClient(mqtt.Client());
    
    if (self.__getConfig().getMqtt().getUsername() != None and self.__getConfig().getMqtt().getPassword() != None):
      self.__getClient().username_pw_set(self.__getConfig().getMqtt().getUsername(), self.__getConfig().getMqtt().getPassword());
	
    self.__getClient().on_connect = self.__onConnect;
    self.__getClient().on_disconnect = self.__onDisconnect;
    self.__getClient().on_message = self.__onMessage;
	
    try:
      self.__getClient().connect(self.__getConfig().getMqtt().getHostname(), self.__getConfig().getMqtt().getPort(), self.__getConfig().getMqtt().getTimeout());
	
      self.__getClient().subscribe((self.__getConfig().getMqtt().getTopicPrefix()  + "/#" if self.__getConfig().getMqtt().getTopicPrefix() != None else "#"), self.__getConfig().getMqtt().getQosSubscribe());
	
      self.__getClient().loop_start();
	  
      for i in range(100):
        if (self.__getConnected()):
          break;
        else:
          time.sleep(0.5);
    except:
      logging.error(traceback.format_exc());
      self.__setClient(None);
	  
  def __setConnected(self, connected):
    self.__connected = connected;	
    
  def __onConnect(self, client, userdata, flags, rc):
  
    logging.info("Connected with result code " + str(rc));
    if (rc != 0):
      logging.error("Connected with result code " + str(rc))
    else:
      self.__setConnected(True);
	  
  def __onDisconnect(self, mqtt_client, userdata, rc):
    self.__getConnected(False);
    logging.error("Diconnected! will reconnect! ...");
	
    if (rc is 0):
      self.connect();
    else:
      time.sleep(5)
      while not self.__getBrokerReachable():
        time.sleep(10)
        self.__getClient().reconnect();
		
  def __getBrokerReachable(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    s.settimeout(5);
	
    try:
      s.connect((self.__getConfig().getMqtt().getHostname(), self.__getConfig().getMqtt().getPort()));
      s.close();
      return True;
    except socket.error:
      return False;
	  
  def __onMessage(self, client, userdata, message):

    topic = message.topic;
	
    if (self.__getConfig().getMqtt().getTopicPrefix() != None):
      topic = topic[len(self.__getConfig().getMqtt().getTopicPrefix()) + 1 :];

    if (topic[0:4] == "set/"):
      logging.info("MQTT " + message.topic + ": " + message.payload);
      self.__getSubscriberMethod()(topic[4:], message.payload);
	
  def publish(self, topic, payload):

    if (self.__getConnected()):
      topic = (self.__getConfig().getMqtt().getTopicPrefix() + "/" if self.__getConfig().getMqtt().getTopicPrefix() != None else "") + "get/" + topic;
      logging.info("MQTT " + topic + ": " + payload);
      self.__getClient().publish(topic, payload=payload, qos=self.__getConfig().getMqtt().getQosPublish(), retain=self.__getConfig().getMqtt().getRetain());
    
  def subscribe(self, method):
    self.__setSubscriberMethod(method);
