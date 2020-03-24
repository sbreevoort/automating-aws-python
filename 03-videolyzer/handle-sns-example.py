# coding: utf-8
event = {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:us-east-1:602635905367:handleLabelDetectionTopic:1b997d08-e0cc-433c-8c35-630bf2895228', 'Sns': {'Type': 'Notification', 'MessageId': '980e4296-261d-5755-b827-14625d1198e7', 'TopicArn': 'arn:aws:sns:us-east-1:602635905367:handleLabelDetectionTopic', 'Subject': None, 'Message': '{"JobId":"b9aa2dc8edecffdc1f67794aba6bb1bad5e47571a2152129f4c5d32f5c9e2ff2","Status":"SUCCEEDED","API":"StartLabelDetection","Timestamp":1585084620784,"Video":{"S3ObjectName":"video.mp4","S3Bucket":"sbrvideolyzervideos"}}', 'Timestamp': '2020-03-24T21:17:00.848Z', 'SignatureVersion': '1', 'Signature': 'PrEF0gPykZeY+/CqXKp9/tmimPDIG6sYfG9nT7DmJLs4W9beCt0RjLmspqsNT/5CsY7dWf1m68L/l/QuLm96ZVaHLcprooj4Gpuq1ePjcSJKUiwR5dv1W6VazgmFL3vnKw3J/900qxKv2UjZZEH5mD+VRcu0uUkbgM1gqT7iOAgqULvM83b2UYMZwTwvBwDmHDdDy/VX9uaRFzDKNUXG3yH62FAMkXU5iK7PHvgcgR8NJpvS8rmZGdzm+L/VD09HB9S0n/Y+ygz7ywk3Y1/A+oMVMKbarQWoX5fOt7uHgP1tMZ74xKuqPZA93M8EKhmwIRjsikrgBDnBU9tnNMBOBg==', 'SigningCertUrl': 'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-a86cb10b4e1f29c941702d737128f7b6.pem', 'UnsubscribeUrl': 'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:602635905367:handleLabelDetectionTopic:1b997d08-e0cc-433c-8c35-630bf2895228', 'MessageAttributes': {}}}]}
event
event['Records'][0]['Sns']
event['Records'][0]['Sns']['Message']
import json
json.loads(event['Records'][0]['Sns']['Message'])['JobId']
json.loads(event['Records'][0]['Sns']['Message'])
get_ipython().run_line_magic('save', 'handle-sns-example.py 1-8')
