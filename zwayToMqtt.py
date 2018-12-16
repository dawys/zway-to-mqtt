#!/usr/bin/env python

import logging;
import sys;

from classes.config import Config;
from classes.mqttClient import MqttClient;
from classes.zwayClient import ZwayClient;

class ZwayToMqtt:

	def __init__(self):
	
		config = Config();

		mqttClient = MqttClient(config);
		zwayClient = ZwayClient(config, mqttClient);
		mqttClient.subscribe(zwayClient.writeDevice);
		zwayClient.start();
 
if __name__ == "__main__":
	ZwayToMqtt();