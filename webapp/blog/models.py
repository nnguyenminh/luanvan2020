from djongo import models
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.

# class Post(models.Model):
#     _id = models.ObjectIdField()
#     # id = models.AutoField()
#     # category = models.CharField(max_length=255)
#     title = models.CharField(max_length=255)
#     content = models.JSONField()
#     comment = models.JSONField()
#     date = models.DateTimeField(auto_now_add=True)
#     # tag = models.JSONField()
#     # author_details = models.JSONField()
#     objects = models.DjongoManager()
#
#     def __str__(self):
#         return f"{self.title}"

class Category(models.Model):
    # _id = models.ObjectIdField()
    name = models.CharField(max_length=255)
    objects = models.DjongoManager()

    def __str__(self):
        return self.name


class Post(models.Model):
    # _id = models.ObjectIdField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(auto_now=False, auto_now_add=False)
    objects = models.DjongoManager()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, related_name='children', null=True)
    name = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{"root" if not self.parent else self.parent} - {self.name}'
