from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from .settings import AWS_STORAGE_BUCKET_NAME, LOCAL_DOWNLOAD_PATH
import boto3
import os

class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION

    def create_dir(dir_name):
        client = boto3.client('s3')
        client.put_object(Bucket= AWS_STORAGE_BUCKET_NAME, Key=dir_name+'/')

    def upload_file(file, user, dir):
        client = boto3.client('s3')
        data = file
        f = open('tempfile', 'wb')
        for chunk in data.chunks():
            f.write(chunk)
        f.close()

        nf = open('tempfile', 'rb')
        # client.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key=file_name, body= nf)
        client.upload_fileobj(nf, AWS_STORAGE_BUCKET_NAME, user.username + '/' + dir + file.name)
        os.remove('tempfile')
        # putResponse = client.put_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key= file_name)

    def download_file(file_name, dir):
        client = boto3.resource('s3')
        client.Bucket(AWS_STORAGE_BUCKET_NAME).download_file(Key= dir, Filename=LOCAL_DOWNLOAD_PATH+file_name)

    def delete_file(file_name, dir):
        client = boto3.resource('s3')
        client.Bucket(AWS_STORAGE_BUCKET_NAME).objects.filter(Prefix=dir).delete()






























































    def print_dir(dir_name):
        s3 = boto3.resource('s3')
        mybucket = s3.Bucket('fileshell-test')
        return(mybucket.objects.all())


