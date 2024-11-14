from django.db import models
from django.urls import reverse


class ServiceNS(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    comments = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class ServiceApp(models.Model):
    service_id = models.CharField(max_length=100, blank=True, null=True)
    namespace = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)
    replicas = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
