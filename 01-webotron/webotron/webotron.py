"""Webotron automates deploying a static website to AWS S3
"""
from pathlib import Path
import mimetypes

import boto3
from botocore.exceptions import ClientError

import click

session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')


@click.group()
def cli():
    """Webotron deploys websites to AWS"""


@cli.command('list-bucket-objects')
@click.argument('bucketname')
def list_bucket_objects(bucketname):
    """List all objects in s3 bucket"""
    for obj in s3.Bucket(bucketname).objects.all():
        print(obj)


@cli.command('list-buckets')
def list_buckets():
    """List all s3 buckets"""
    for bucket in s3.buckets.all():
        print(bucket)


@cli.command('setup-bucket')
@click.argument('bucketname')
def setup_bucket(bucketname):
    """Create and configure a bucket"""

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

    pol = s3_bucket.Policy()
    pol.put(Policy=policy)

    website = s3_bucket.Website()
    website.put(WebsiteConfiguration={
        'ErrorDocument': {
            'Key': 'error.html'
        },
        'IndexDocument': {
            'Suffix': 'index.html'
        }
    })



def upload_file(s3_bucket, path, key):
    """Upload file to S3"""
    content_type = mimetypes.guess_type(key)[0] or 'text/plain'
    print('Contenttype: {}'.format(content_type))
    s3_bucket.upload_file(
        path,
        key,
        ExtraArgs={
            'ContentType': content_type
        }
    )


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync contents of [pathname] to bucket"""
    s3_bucket = s3.Bucket(bucket)
    root = Path(pathname).resolve()

    def handle_dir(target):
        for p in target.iterdir():
            if p.is_dir():
                handle_dir(p)
            if p.is_file():
                print('Path: {}\nKey: {}'.format(p, p.relative_to(root).as_posix()))
                upload_file(s3_bucket, str(p), str(p.relative_to(root).as_posix()))

    handle_dir(root)


if __name__ == '__main__':
    cli()
