import boto3
import click
from botocore.exceptions import ClientError

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

@cli.command('setup-bucket')
@click.argument('bucketname')
def setup_bucket(bucketname):
    "Create and configure a bucket"

    s3_bucket = None
    try:
        s3_bucket = s3.create_bucket(
            Bucket=bucketname,
            CreateBucketConfiguration={'LocationConstraint': session.region_name}
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            s3_bucket = s3.Bucket(bucketname)
        else:
            raise e

    policy = """
    {
      "Version":"2012-10-17",
      "Statement":[
        {
          "Sid":"PublicRead",
          "Effect":"Allow",
          "Principal": "*",
          "Action":["s3:GetObject"],
          "Resource":["arn:aws:s3:::%s/*"]
        }
      ]
    }
    """ % s3_bucket.name
    policy = policy.strip()

    pol=s3_bucket.Policy()
    pol.put(Policy=policy)

    website=s3_bucket.Website()
    website.put(WebsiteConfiguration={
       'ErrorDocument': {
           'Key': 'error.html'
       },
       'IndexDocument': {
           'Suffix': 'index.html'
       }
    })

    return

if __name__ == '__main__':
    cli()
