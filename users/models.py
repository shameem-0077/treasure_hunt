from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    game = models.ForeignKey("hunts.TreasureHuntGame", on_delete=models.CASCADE, related_name='players')
    score = models.IntegerField(default=0)
    current_question = models.IntegerField(default=1)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.game.name}"
