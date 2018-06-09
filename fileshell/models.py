from django.db import models

class File(models.Model):
    title = models.CharField(max_length=100)
    user = models.CharField(max_length=20)
    uploaded_TM = models.DateTimeField(auto_now_add=True)
    last_view_TM = models.DateTimeField(auto_now_add=True)
    isFavor = models.BooleanField(default=False)
    bucketPath = models.CharField(max_length=50)
    fileSize = models.IntegerField()
    folder = models.ForeignKey('Folder', null=True, blank=True, related_name='datas')

class Folder(models.Model):
    dir_name = models.CharField(max_length=30)
    user = models.CharField(max_length=20, default='')
    parent = models.ForeignKey('self', related_name='child', null=True, blank=True)