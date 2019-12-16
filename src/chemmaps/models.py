from django.db import models


class Name(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class UploadFile(models.Model):
    docfile = models.FileField(upload_to='temp/')
