from troposphere import Ref
from troposphere import s3

class BucketResource:
    def __init__(self, BucketName):
        self.BucketName = BucketName

    def getResource(self):
        return s3.Bucket(title="Bucket", **{
            'BucketName': Ref(self.BucketName)
        })