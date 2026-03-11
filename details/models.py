from django.db import models
from userauth.models import User

class match(models.Model):
    player = models.ForeignKey(User,on_delete=models.CASCADE, related_name='player', null=True)
    win = models.IntegerField(default=0)
    lose = models.IntegerField(default=0)
    draw = models.IntegerField(default=0)
    gs = models.IntegerField(default=0)
    gc = models.IntegerField(default=0)
    hatrick = models.IntegerField(default=0)
    motm = models.BooleanField(default=False)

    def __str__(self):
        return self.player.username


class news(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    image = models.URLField(max_length=200)

    def __str__(self):
        return self.title

