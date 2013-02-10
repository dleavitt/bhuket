import uuid
from string import Template
from boto.iam.connection import IAMConnection
from boto.s3.connection import S3Connection
from boto.exception import BotoServerError


class Bucketier:
    "Our brave worker. Wrangler of the bucket."

    def __init__(self, bucket_name, aws_key, aws_secret):
        # smell?
        self.redis = self.__class__.redis

        self.job_id = str(uuid.uuid1())
        self.bucket_name = bucket_name
        self.aws_key = aws_key
        self.aws_secret = aws_secret

        # TODO: clean up bucket name string? What's a valid AWS username?
        self.user_name = "bhuket-" + bucket_name

        self.iam = IAMConnection(aws_key, aws_secret)
        self.s3 = S3Connection(aws_key, aws_secret)
        self.status = ':|'

    def run(self):
        self.create_user()
        self.create_bucket()
        self.status = ':)'

    def to_json(self):
        return {
            'job_id': self.job_id,
            'bucket_name': self.bucket_name,
            'status': self.status
        }

    def create_user(self):
        # TODO: check creds
        # TODO: checking responses would be a good thing
        try:
            self.iam.create_user(self.user_name)
        except BotoServerError as ex:
            # is it because the user already exists? that's fine, carry on
            if ex.status != 409:
                # TODO: mark it as failed and move on
                raise ex

        self.iam.put_user_policy(self.user_name, "bucket-access", self.policy_template())

    def create_bucket(self):
        # TODO: check if name has been taken, etc
        self.s3.create_bucket(self.bucket_name)

    def validate(self):
        for attr in 'bucket_name aws_key aws_secret'.split():
            if not getattr(self, attr):
                return False

        # TODO: validate bucket name format
        return True

    def policy_template(self):
        policy_template = open('templates/policy_template.json').read()
        return Template(policy_template).substitute(bucket_name=self.bucket_name)
