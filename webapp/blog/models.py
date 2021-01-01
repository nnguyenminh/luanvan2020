from djongo import models
# from autoslug import AutoSlugField
from django.utils.text import slugify


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
    name = models.CharField(max_length=255)
    objects = models.DjongoManager()

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    title_vn = models.CharField(max_length=255)
    content = models.TextField()
    content_vn = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    # publish = models.DateTimeField(auto_now=False, auto_now_add=False)
    objects = models.DjongoManager()

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, related_name='children', null=True)
    reply = models.CharField(max_length=100, editable=False)
    author = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    hidden = models.BooleanField(default=False)
    flag = models.BooleanField(default=False)

    group = models.SlugField(
        default='',
        editable=False,
    )

    def save(self, *args, **kwargs):
        if self.parent:
            if self.parent.group != "0":
                value = self.parent.group
            else:
                value = self.parent.id
        else:
            value = 0
        self.group = slugify(value, allow_unicode=True)

        if self.parent:
            self.reply = f'Reply @{self.parent.author}'
        else:
            self.reply = ""
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Post:{self.post}/Group:{self.group}/Author:{self.author}'
