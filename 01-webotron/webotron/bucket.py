""" Class for S3 buckets"""
import mimetypes
import boto3
from functools import reduce
from botocore.exceptions import ClientError
from pathlib import Path
from pprint import pprint
from hashlib import md5


from webotron import util


class BucketManager:
    """Manage S3"""

    CHUNK_SIZE = 8388608

    def __init__(self, session):
        """Create a BucketManager object"""
        self.session = session
        self.s3 = self.session.resource('s3')
        self.transfer_config = boto3.s3.transfer.TransferConfig(
            multipart_chunksize = self.CHUNK_SIZE,
            multipart_threshold = self.CHUNK_SIZE
        )
        self.manifest = {}

    def get_region_name(self, s3_bucket):
        """Get region name of s3_bucket"""
        bucket_location = self.s3.meta.client.get_bucket_location(Bucket=s3_bucket.name)
        return bucket_location["LocationConstraint"]


    def get_bucket_url(self, s3_bucket):
        """Get website url for this bucket"""
        return "http://{}.{}".format(s3_bucket.name
        , util.get_endpoint(self.get_region_name(s3_bucket)).host)


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

    def load_manifest(self, s3_bucket):
        """Load mainfest"""
        paginator = self.s3.meta.client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=s3_bucket.name):
            for obj in page.get('Contents', []):
                self.manifest[obj['Key']] = obj['ETag']
                #pprint(obj)


    @staticmethod
    def hash_data(data):
        """Generate md5 hash for data"""
        hash = md5()
        hash.update(data)
        return hash

    def generate_etag(self, filename):
        """Generate Etag for file"""
        hashes = []
        with open(filename, 'rb') as f:
            while True:
                data = f.read(self.CHUNK_SIZE)
                if not data:
                    break
                hashes.append(self. hash_data(data))

        if not hashes:  # emptyfile
            return
        elif len(hashes)==1:   # 1 chunk
            return '"{}"'.format(hashes[0].hexdigest())
        else:    # meerdere hashes, die ook weer gehasht worden
            hash = self.hash_data(reduce(lambda x,y: x+y, (h.digest for h in hashes) ))
            return '"{}-{}"'.format(hash.hexdigest(), len(hashes))


    def upload_file(self, s3_bucket, path, key):
        """Upload file to S3"""
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'

        etag = self.generate_etag(path)
        if self.manifest.get(key, '') == etag:   # bestand is niet gewijzigd
            print("Skipping {}, etags match".format(key))
            return

        print('Contenttype: {}'.format(content_type))
        return s3_bucket.upload_file(
            path,
            key,
            ExtraArgs={
                'ContentType': content_type
            },
            Config=self.transfer_config
        )

    def sync(self, pathname, bucketname):
        s3_bucket = self.s3.Bucket(bucketname)
        self.load_manifest(s3_bucket)

        root = Path(pathname).resolve()

        def handle_dir(target):
            for p in target.iterdir():
                if p.is_dir():
                    handle_dir(p)
                if p.is_file():
                    print('Path: {}\nKey: {}'.format(p, p.relative_to(root).as_posix()))
                    self.upload_file(s3_bucket, str(p), str(p.relative_to(root).as_posix()))

        handle_dir(root)
