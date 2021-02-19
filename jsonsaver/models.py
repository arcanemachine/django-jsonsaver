from django.db import models


class JsonItem(models.Model):
    message = models.TextField()
