import uuid
from string import Template
from boto.iam.connection import IAMConnection
from boto.s3.connection import S3Connection
from boto.exception import BotoServerError


class Bucketier:
    "Our brave worker. Wrangler of the bucket."

    class BucketierException(StandardError):
        pass

    def __init__(self, bucket_name, aws_key, aws_secret):
        self.job_id = str(uuid.uuid1())
        self.bucket_name = bucket_name
        self.aws_key = aws_key
        self.aws_secret = aws_secret

        # TODO: clean up bucket name string? What's a valid AWS username?
        self.user_name = "bhuket-" + bucket_name

        self.iam = IAMConnection(aws_key, aws_secret)
        self.s3 = S3Connection(aws_key, aws_secret)

    def run(self):
        try:
            self.create_user()
            self.create_bucket()
        except BotoServerError as ex:
            if ex.code == 'InvalidClientTokenId':
                raise self.BucketierException("Bad AWS creds - did you enter them right?")
            else:
                print ex
                raise self.BucketierException(ex.error_message)

    def to_json(self):
        return {
            'user_name': self.user_name,
            'bucket_name': self.bucket_name,
            'bucket_url': "https://s3.amazonaws.com/%s/" % self.bucket_name,
            'aws_key': self.user_aws_key,
            'aws_secret': self.user_aws_secret
        }

    def create_user(self):
        try:
            self.iam.create_user(self.user_name)
        except BotoServerError as ex:
            if ex.code == 'EntityAlreadyExists':
                # is it because the user already exists?
                # just run it again with a random name
                self.user_name = self.user_name + "-" + uuid.uuid1().hex[0:12]
                return self.create_user()
            else:
                # TODO: mark it as failed and move on
                raise ex

        key_response = self.iam.create_access_key(self.user_name)
        # TODO: catch this if it blows up
        key = key_response['create_access_key_response']['create_access_key_result']['access_key']
        self.user_aws_key = key['access_key_id']
        self.user_aws_secret = key['secret_access_key']

        self.iam.put_user_policy(self.user_name, "bucket-access", self.policy_template())

        return (self.user_name, self.user_aws_key, self.user_aws_secret)

    def create_bucket(self):
        # TODO: check if name has been taken, etc
        return self.s3.create_bucket(self.bucket_name)

    def validate(self):
        for attr in 'bucket_name aws_key aws_secret'.split():
            if not getattr(self, attr):
                return False

        # TODO: validate bucket name format
        return True

    def policy_template(self):
        policy_template = open('templates/policy_template.json').read()
        return Template(policy_template).substitute(bucket_name=self.bucket_name)
