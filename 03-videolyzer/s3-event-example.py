# coding: utf-8
event = {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-1', 'eventTime': '2020-03-22T21:22:43.250Z', 'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'AWS:AIDAYYT7GFFL7VJRFSVOO'}, 'requestParameters': {'sourceIPAddress': '94.210.202.41'}, 'responseElements': {'x-amz-request-id': 'ACC6B6E3BFD4BD45', 'x-amz-id-2': 'vBHcNUkKs11D5FDGz+XydSFddIAHAAagICXpURjYMoTKXJNq26Irzh0xugLzvSB9uP+HUtiDEKAbz/7fWjGSpY/8qe5Z29Jk'}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': '2f2b7551-54ce-4a22-990a-0b25b34695eb', 'bucket': {'name': 'sbrvideolyzervideos', 'ownerIdentity': {'principalId': 'AMEA3UQR5WTL6'}, 'arn': 'arn:aws:s3:::sbrvideolyzervideos'}, 'object': {'key': 'video.mp4', 'size': 7165017, 'eTag': '75b2c410fcdc095518f680e63fe77e50', 'sequencer': '005E77D7066EC257C8'}}}]}
event
{'Records': [{'eventVersion': '2.1',
   'eventSource': 'aws:s3',
   'awsRegion': 'us-east-1',
   'eventTime': '2020-03-22T21:22:43.250Z',
   'eventName': 'ObjectCreated:Put',
   'userIdentity': {'principalId': 'AWS:AIDAYYT7GFFL7VJRFSVOO'},
   'requestParameters': {'sourceIPAddress': '94.210.202.41'},
   'responseElements': {'x-amz-request-id': 'ACC6B6E3BFD4BD45',
    'x-amz-id-2': 'vBHcNUkKs11D5FDGz+XydSFddIAHAAagICXpURjYMoTKXJNq26Irzh0xugLzvSB9uP+HUtiDEKAbz/7fWjGSpY/8qe5Z29Jk'},
   's3': {'s3SchemaVersion': '1.0',
    'configurationId': '2f2b7551-54ce-4a22-990a-0b25b34695eb',
    'bucket': {'name': 'sbrvideolyzervideos',
     'ownerIdentity': {'principalId': 'AMEA3UQR5WTL6'},
     'arn': 'arn:aws:s3:::sbrvideolyzervideos'},
    'object': {'key': 'video.mp4',
     'size': 7165017,
     'eTag': '75b2c410fcdc095518f680e63fe77e50',
     'sequencer': '005E77D7066EC257C8'}}}]}
event['Records'][0]['s3']['bucket']['name']
event['Records'][0]['s3']['object']['key']
import urllib
urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
