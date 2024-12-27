import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    game = models.ForeignKey("hunts.TreasureHuntGame", on_delete=models.CASCADE, related_name='players')
    unique_id = models.UUIDField(unique=True)
    score = models.IntegerField(default=0)
    current_question = models.IntegerField(default=1)
    finished = models.BooleanField(default=False)

    def save(self, request=None, *args, **kwargs):
        if self._state.adding:
            unique_id = uuid.uuid4()
            while Player.objects.filter(unique_id=unique_id).exclude(pk=self.pk).exists():
                unique_id = uuid.uuid4()

            self.unique_id = unique_id

        super(Player, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.game.name}"
