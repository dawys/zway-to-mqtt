# zwayToMqtt.py

zwayToMqtt.py is intended to run as a service, it connects to [z-way-server] and pushes the defined devices to MQTT

A running [z-way-server](https://z-wave.me/z-way/download-z-way/) and a mqtt-broker (e.g: [mosquitto](https://mosquitto.org)) are required to use this deamon.

## Usage

## Example

## Configuration file

a self explaining sample configuration file is included 
copy config.xml.sample to config.xml

## Libs required
the following libraries are required by onewireToMqtt.py
- python-requests
- python-pip
- python-enum
- paho-mqt

install with
```
apt-get install python-requests python-pip python-enum
pip install paho-mqt
```
