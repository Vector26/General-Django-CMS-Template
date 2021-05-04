from django.db import models
from Profile.models import Profile
from django.utils import timezone
# Create your models here.

class PostContent(models.Model):
    profile=models.ForeignKey(Profile,related_name="profile",on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.TextField(max_length=1000)

    def __str__(self):
        if(len(self.content)>15):
            return self.content[:15]+"..."
        else:
            return self.content

    def getLikes(self):
        return Likes.objects.filter(post=self).count()

    def getComments(self):
        return Comment.objects.filter(post=self)

class Likes(models.Model):
    post=models.ForeignKey(PostContent,related_name="LikedPost",on_delete=models.CASCADE)
    liker=models.ForeignKey(Profile,related_name="liker",on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post} liked by '{self.liker}'"

class Comment(models.Model):
    post=models.ForeignKey(PostContent,related_name="postofComment",on_delete=models.CASCADE)
    comment=models.TextField(max_length=1000,default="")
    commenter=models.ForeignKey(Profile,related_name="commenter",on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.commenter} Commented '{self.comment}' on {self.post.profile}'s Post"