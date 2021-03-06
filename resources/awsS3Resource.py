import os
import boto3
import io
from .S3AudioObject import S3AudioObject

class AwsS3Resource:

    def __init__(self):
        session = boto3.Session(aws_access_key_id=os.environ['AWS_KEY'],
                                aws_secret_access_key=os.environ['AWS_SECRET'])
        s3 = session.resource('s3')
        self.bucket = s3.Bucket(os.environ['BUCKET_NAME'])

    def get_stream_data(self, file_name):
        s3_object = self.bucket.Object(file_name)
        audio_stream = io.BytesIO()
        metadata = s3_object.metadata
        s3_object.download_fileobj(audio_stream)
        audio_data = S3AudioObject(metadata, audio_stream.getvalue())
        return audio_data

    def remove_file(self, file_name):
        file = self.bucket.Object(file_name)
        file.delete()
