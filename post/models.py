from django.db import models
from user.models import User


class Post(models.Model):
    class Meta:
        db_table = 'post'

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256, null=False)
    postdate = models.DateTimeField(null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __repr__(self):
        return '<Post {} {} {} {} >'.format(
            self.id, self.title, self.author_id, self.content
        )

    __str__ = __repr__


class Content(models.Model):
    class Meta:
        db_table = 'content'

    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    content = models.TextField(null=False)

    def __repr__(self):
        return '<Content {} {}>'.format(self.post.id, self.content[:20])

    __str__ = __repr__
