# coding: utf-8
import boto3
session = boto3.Session(profile_name='pythonAutomation')
as_client = session.client('autoscaling')
as_client.describe_auto_scaling_groups
as_client.describe_auto_scaling_groups()
as_client.describe_policies()
as_client.execute_policy(AutoScalingGroupName='AS Notifon Example', PolicyName='Scale down')
as_client.execute_policy(AutoScalingGroupName='AS Notifon Example', PolicyName='Scale up')
