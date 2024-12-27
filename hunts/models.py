from django.db import models

# Create your models here.

class TreasureHuntGame(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    QUESTION_TYPE_CHOICES = (
        ("text", "Text"),
        ('image', "Image"),
        ('video', 'Video'),
        ("document", "Document")
    )
    game = models.ForeignKey(TreasureHuntGame, on_delete=models.CASCADE, related_name='questions')
    order = models.IntegerField()
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    answer = models.CharField(max_length=255)
    hint = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=255, choices=QUESTION_TYPE_CHOICES, default="text")
    attachment = models.FileField(upload_to='questions/attachments/', blank=True, null=True)

    def __str__(self):
        return f"Question {self.order} for {self.game.name}"

    class Meta:
        unique_together = ('game', 'order')
        ordering = ['order']

class PlayerProgress(models.Model):
    player = models.ForeignKey("users.Player", on_delete=models.CASCADE, related_name='progress')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.player.user.username} progress on Question {self.question.order}"
