# coding:UTF-8
import boto3
import json
import logging
import os

from base64 import b64decode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from botocore.vendored import requests

print('Loading function')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

url = "https://notify-api.line.me/api/notify"
token = "LineApiTOKEN"


def lambda_handler(event, context):
    logger.info("Event: " + str(event))
    message_unicode = json.loads(event['Records'][0]['Sns']['Message'])
    logger.info("Message: " + str(message_unicode))
    alarm_name = message_unicode['AlarmName']
    # old_state = message['OldStateValue']
    new_state = message_unicode['NewStateValue']
    reason = message_unicode['NewStateReason']
    message = "%s state is now %s: %s" % (alarm_name, new_state, reason)

    stickerPackageId = 2

    stickerId = 152

    headers = {"Authorization": "Bearer " + token}

    payload = {"message": message, "stickerPackageId": stickerPackageId, "stickerId": stickerId}

    r = requests.post(url, headers=headers, data=payload)
    # try:
    #     response = urlopen(req)
    #     response.read()
    #     logger.info("Message posted to %s", message)
    # except HTTPError as e:
    #     logger.error("Request failed: %d %s", e.code, e.reason)
    # except URLError as e:
    #     logger.error("Server connection failed: %s", e.reason)


