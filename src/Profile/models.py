from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,related_name='ProfileUser',on_delete=models.CASCADE)
    Bio=models.CharField(max_length=150,default="Bio Here")
    DOB=models.DateField(default=datetime.date(1990,1,1))
    image = models.ImageField(default='default.png')

    def getUsername(self):
        # user_id=User.objects.get(username=self.user.username)
        return self.user.username

    def getFollowersCount(self):
        return FollowerSystem.objects.filter(FollowedUser=self).count()

    def getFollowedCount(self):
        return FollowerSystem.objects.filter(Follower=self).count()

    def __str__(self):
        return f"{self.getUsername()}"

class FollowerSystem(models.Model):
    FollowedUser=models.ForeignKey(Profile,related_name="FollowedUser",on_delete=models.CASCADE)
    Follower=models.ForeignKey(Profile,related_name="Follower",on_delete=models.CASCADE)
    Date=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.Follower.user.username} follows {self.FollowedUser.user.username}"