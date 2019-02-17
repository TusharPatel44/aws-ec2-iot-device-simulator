# Simulate random moisture levels.
# This script is based on the AWS IoT additional tutorial
# with additional modification.

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import random
import time
import logging
import argparse

# Read command-line parameters
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-e", "--endpoint", required=True, dest="host", help="Your AWS Iot endpoint")
arg_parser.add_argument("-r", "--rootCA", required=True, dest="rootCAPath", help="Root CA file path")
arg_parser.add_argument("-c", "--cert", required=True, dest="certPath", help="Certificate path")
arg_parser.add_argument("-k", "--key", required=True, dest="privateKeyPath", help="Private key file path")
arg_parser.add_argument("-d", "--delay", required=False, default=5, help="delay in seconds")

args = arg_parser.parse_args()
hostName    = args.host
rootCAPath  = args.rootCAPath
certPath    = args.certPath
privKeyPath = args.privateKeyPath 
delayTime   = int(args.delay)
port        = 8883

# shadow client 
shadow_handler   = "Ec2-001"
shadow_client_id = "moist-shadow-client"

# callback
def shadowUpdateCallback(payload, responseStatus, token):
  print("Shadow update callback: ")
  print('UPDATE: $aws/things/' + shadow_handler + '/shadow/update/#')
  print()

# configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)


# client creation, configuration, and connection
shadow_client = AWSIoTMQTTShadowClient(shadow_client_id)
shadow_client.configureEndpoint(hostName, port)
shadow_client.configureCredentials(rootCAPath, privKeyPath, certPath)
shadow_client.configureConnectDisconnectTimeout(10)
shadow_client.configureMQTTOperationTimeout(5)
shadow_client.connect()

# create a programmatic representation of the shadow
device_shadow = shadow_client.createShadowHandlerWithName(shadow_handler, True)

while True:
  moisture = random.choice([True, False])

  if moisture:
    device_shadow.shadowUpdate('{"state":{"reported":{"moisture":"okay"}}}', 
    shadowUpdateCallback, 5)
  else:
    device_shadow.shadowUpdate('{"state":{"reported":{"moisture":"low"}}}',
    shadowUpdateCallback, 5)

  time.sleep(delayTime)

