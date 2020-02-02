""" Class for S3 buckets"""
import mimetypes
from botocore.exceptions import ClientError
from pathlib import Path


class BucketManager:
    """Manage S3"""

    def __init__(self, session):
        """Create a BucketManager object"""
        self.session = session
        self.s3 = self.session.resource('s3')

    def all_buckets(self):
        """Iterator for all buckets"""
        return self.s3.buckets.all()

    def all_objects(self, bucketname):
        """Iterator for all objects in bucket"""
        return self.s3.Bucket(bucketname).objects.all()

    def init_bucket(self, bucketname):
        """Setup a bucket"""
        s3_bucket = None
        try:
            s3_bucket = self.s3.create_bucket(
                Bucket=bucketname,
                CreateBucketConfiguration={'LocationConstraint': self.session.region_name}
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                s3_bucket = self.s3.Bucket(bucketname)
            else:
                raise e

        return s3_bucket

    def set_policy(self, s3_bucket):
        """Set bucket policy to public"""
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

    def configure_website(self, s3_bucket):
        website = s3_bucket.Website()
        website.put(WebsiteConfiguration={
            'ErrorDocument': {
                'Key': 'error.html'
            },
            'IndexDocument': {
                'Suffix': 'index.html'
            }
        })

    def upload_file(self, s3_bucket, path, key):
        """Upload file to S3"""
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'
        print('Contenttype: {}'.format(content_type))
        return s3_bucket.upload_file(
            path,
            key,
            ExtraArgs={
                'ContentType': content_type
            }
        )

    def sync(self, pathname, bucketname):
        s3_bucket = self.s3.Bucket(bucketname)

        root = Path(pathname).resolve()

        def handle_dir(target):
            for p in target.iterdir():
                if p.is_dir():
                    handle_dir(p)
                if p.is_file():
                    print('Path: {}\nKey: {}'.format(p, p.relative_to(root).as_posix()))
                    self.upload_file(s3_bucket, str(p), str(p.relative_to(root).as_posix()))

        handle_dir(root)
