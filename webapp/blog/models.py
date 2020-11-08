from djongo import models


# Create your models here.

class Post(models.Model):
    _id = models.ObjectIdField()
    # id = models.AutoField()
    category = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.JSONField()
    comment = models.JSONField()
    date = models.DateTimeField(auto_now_add=True)
    # tag = models.JSONField()
    # author_details = models.JSONField()
    objects = models.DjongoManager()
