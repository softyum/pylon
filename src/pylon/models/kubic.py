from django.db import models
from django.urls import reverse


class KubeNs(models.Model):
    name = models.CharField(max_length=200)
    comments = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class KubeApp(models.Model):
    app_name = models.CharField(max_length=100)
    namespace = models.CharField(max_length=200)
    image = models.CharField(max_length=500)

    def __str__(self):
        return self.name
