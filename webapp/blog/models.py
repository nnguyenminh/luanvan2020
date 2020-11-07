from djongo import models


# Create your models here.

class Post(models.Model):
    _id = models.ObjectIdField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    comment = models.JSONField()
    date = models.DateField()
    # tag = models.JSONField()
    # author_details = models.JSONField()
    objects = models.DjongoManager()
