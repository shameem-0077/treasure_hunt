from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Player
from hunts.models import PlayerProgress, Question, TreasureHuntGame

@receiver(post_save, sender=PlayerProgress)
def assign_next_question(sender, instance, created, **kwargs):
    if instance.is_completed:
        last_question = Question.objects.filter(game=instance.player.game).distinct().order_by('-order').first()

        if last_question != instance.question:
            game = instance.player.game
            next_order_id = instance.player.current_question + 1
            instance.player.current_question = next_order_id
            instance.player.save()
            question = Question.objects.get(game=game, order=next_order_id)
            player_progres = PlayerProgress.objects.create(
                player=instance.player,
                question=question
            )
            