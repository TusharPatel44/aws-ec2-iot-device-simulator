# aws-ec2-iot-device-simulator

Simple AWS IoT device simulator in Python. The simulator scripts run on AWS EC2 instance.

## Getting Started

### Prerequisites

* Amazon AWS account

### Overview
The cloudformation template will create a t2.micro AWS EC2 instance as the 'thing' or 'device'. 
The device (ec2 instance) requires identification in order to connect to the AWS IoT.
After identification document is ready and installed, the python script that produce the data (act as device) can be run. 

## Devices

### Moisture sensor
It publishes message using MQTT on port 8883. It will update its device shadow.

Usage:
```
moisture_sensor.py [-h] -e HOST -r ROOTCAPATH -c CERTPATH -k PRIVATEKEYPATH [-d DELAY]
```
