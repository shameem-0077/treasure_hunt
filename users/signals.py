from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Player
from hunts.models import PlayerProgress, Question, TreasureHuntGame

@receiver(post_save, sender=Player)
def create_player_progress(sender, instance, created, **kwargs):
    if created:
        game = instance.game
        question = Question.objects.filter(game=game, order=1).order_by('?').first()
        player_progres = PlayerProgress.objects.create(
            player=instance,
            question=question
        )