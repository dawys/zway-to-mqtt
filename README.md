# zwayToMqtt.py

zwayToMqtt.py is intended to run as a service, it connects to [z-way-server] and pushes the defined devices to MQTT

A running [z-way-server](https://z-wave.me/z-way/download-z-way/) and a mqtt-broker (e.g: [mosquitto](https://mosquitto.org)) are required to use this deamon.

## Usage

- install a broker like mosquitto
```
apt-get install mosquitto mosquitto-clients
```

- install software
```
apt-get install python-requests python-pip python-enum
pip install paho-mqtt

cd /usr/local/src

git clone https://github.com/dawys/zway-to-mqtt zwayToMqtt

cd zwayToMqtt

cp config.xml.sample config.xml

cp zway-to-mqtt.service /etc/systemd/system/

systemctl enable zway-to-mqtt.service

vi config.xml

systemctl start zway-to-mqtt.service
```
- edit config to your needs
```
<mqtt>
  <hostname>localhost</hostname>
  <port>1883</port>
  <username>username</username>
  <password>password</password>
</mqtt>

<zway>
  <hostname>localhost</hostname>
  <port>8083</port>
  <username>username</username>
  <password>password</password>
</zway>
```
- map your zway devices to topics
```
<mqtt>
  <topics>
    <topic id="2-1-38" property="switch" type="ON_OFF">diningRoom/light1Switch</topic>
    <topic id="2-1-38" property="dimmer" type="INTEGER">diningRoom/light1Dimmer</topic>
    <topic id="2-1-49-4" type="FLOAT">diningRoom/light1ElectricMeterWatt</topic>
    <topic id="12-0-128" type="INTEGER">basement/smokeDetectorBatteryLevel</topic>
  </topics>
</mqtt>
```

## Example
check if ist is working
```
mosquitto_sub -h localhost -u username -P password -v -t '#'

zway/get/diningRoom/light1Switch ON
zway/get/diningRoom/light1Dimmer 46
zway/get/diningRoom/light1ElectricMeterWatt 22.1
```
if you want to set values
```
mosquitto_pub -h localhost -u username -P password -t zway/set/diningRoom/light1Switch -m OFF
mosquitto_pub -h localhost -u username -P password -t zway/get/diningRoom/light1Dimmer -m 10
```
if you want to init all devices
```
mosquitto_pub -h localhost -u username -P password -t zway/set/init -m true
```

if you are usinf openHAB2 to read and write values
- install binding mqtt and edit services/mqtt.cfg
- define items
```
Item itemDiningRoomLight1Switch {mqtt=">[broker:zway/set/diningRoom/light1Switch:*:default], <[broker:zway/get/diningRoom/light1Switch:*:default], autoupdate="false"}
Item itemDiningRoomLight1Dimmer {mqtt=">[broker:zway/set/diningRoom/light1Dimmer:*:default], <[broker:zway/get/diningRoom/light1Dimmer:*:default], autoupdate="false"}
Item itemDiningRoomLight1ElectricMeterWatt {mqtt="<[broker:zway/get/diningRoom/light1ElectricMeterWatt:*:default]"}
```

## Configuration file

a self explaining sample configuration file is included 
copy config.xml.sample to config.xml

## Libs required
the following libraries are required by zwayToMqtt.py
- python-requests
- python-pip
- python-enum
- paho-mqtt

install with
```
apt-get install python-requests python-pip python-enum
pip install paho-mqtt
```
