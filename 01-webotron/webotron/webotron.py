"""Webotron automates deploying a static website to AWS S3
"""
import boto3
import click
from bucket import BucketManager

session = None
bucket_manager = None

@click.group()
@click.option('--profile', default=None, help='Use a AWS profile')
def cli(profile):
    """Webotron deploys websites to AWS"""
    global session, bucket_manager
    session_cfg = {}
    session_cfg['profile_name'] = profile
    session = boto3.Session(**session_cfg)
    bucket_manager = BucketManager(session)


@cli.command('list-bucket-objects')
@click.argument('bucketname')
def list_bucket_objects(bucketname):
    """List all objects in s3 bucket"""
    for obj in bucket_manager.all_objects(bucketname):
        print(obj)


@cli.command('list-buckets')
def list_buckets():
    """List all s3 buckets"""
    for bucket in bucket_manager.all_buckets():
        print(bucket)


@cli.command('setup-bucket')
@click.argument('bucketname')
def setup_bucket(bucketname):
    """Create and configure a bucket"""

    s3_bucket = bucket_manager.init_bucket(bucketname)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucketname')
def sync(pathname, bucketname):
    """Sync contents of [pathname] to bucket"""
    bucket_manager.sync(pathname, bucketname)


if __name__ == '__main__':
    cli()
