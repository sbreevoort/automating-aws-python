# coding: utf-8
import boto3
from pathlib import Path

session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')

bucket = s3.create_bucket(Bucket='stefanvideolyzervideos',CreateBucketConfiguration={'LocationConstraint': session.region_name})


pathname = 'video.mp4'
path= Path(pathname).expanduser().resolve()

bucket.upload_file(str(path),str(path.name))
rekognition_client = session.client('rekognition')
response = rekognition_client.start_label_detection(Video={'S3Object': {'Bucket': bucket.name, 'Name': path.name}})

response['JobId']
job_id = response['JobId']
result = rekognition_client.get_label_detection(JobId=job_id)
result
result.keys()
result['JobStatus']
result['VideoMetadata']
result['Labels']
len(result['Labels'])
