import boto3
import click

session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')

@click.group()
def cli():
    "Webotron deploys websites to AWS"
    pass

@cli.command('list-bucket-objects')
@click.argument('bucketname')
def list_bucket_objects(bucketname):
    "List all objects in s3 bucket"
    for obj in s3.Bucket(bucketname).objects.all():
	       print(obj)

@cli.command('list-buckets')
def list_buckets():
    "List all s3 buckets"
    for bucket in s3.buckets.all():
        print(bucket)

if __name__ == '__main__':
    cli()
