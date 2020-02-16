# coding: utf-8
import boto3
session = boto3.Session(profile_name='pythonAutomation')
ec2=session.resource('ec2')
key_name = 'python_automation_key'
key_path = key_name + '.pem'
key = ec2.create_key_pair(KeyName=key_name)
key.key_material
with open(key_path, 'w') as key_file:
    key_file.write(key.key_material)
import os, stat
os.chmod(key_path, stat.S_IRUSR|stat.S_IWUSR)
ec2.images.filter(Owners=['amazon'])
img = ec2.Image('ami-099a8245f5daa82bf')
img.name
ami_name = 'amzn2-ami-hvm-2.0.20200207.1-x86_64-gp2'
ami_name_filter = [{'Name':'name', 'Values':[ami_name]}]
list(ec2.images.filter(Owners=['amazon'], Filters=ami_name_filter))
ec2_useast1 = session.resource('ec2', region_name='us-east-1')
ami_name = 'amzn2-ami-hvm-2.0.20200207.1-x86_64-gp2'
ami_name_filter = [{'Name':'name', 'Values':[ami_name]}]
list(ec2_useast1.images.filter(Owners=['amazon'], Filters=ami_name_filter))
img.id
instances = ec2.create_instances(ImageId=img.id, MinCount=1, MaxCount=1, InstanceType='t3.micro', KeyName=key.key_name)
instances
instances[0].terminate()
instances = ec2.create_instances(ImageId=img.id, MinCount=1, MaxCount=1, InstanceType='t3.micro', KeyName=key.key_name)
inst = instances[0]
inst
inst.public_dns_name
inst.wait_until_running()
inst.reload()
inst.security_groups[0]['GroupId']
security_group = ec2.SecurityGroup(inst.security_groups[0]['GroupId'])
security_group.authorize_ingress(IpPermissions=[{'FromPort':22, 'ToPort':22, 'IpProtocol':'TCP', 'IpRanges':[{'CidrIp':'94.210.202.41/32'}]}])
security_group.authorize_ingress(IpPermissions=[{'FromPort':80, 'ToPort':80, 'IpProtocol':'TCP', 'IpRanges':[{'CidrIp':'0.0.0.0/0'}]}])
inst.public_dns_name
get_ipython().run_line_magic('history', '')
