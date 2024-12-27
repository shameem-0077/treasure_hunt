from django.contrib import admin
from .models import TreasureHuntGame, Question, PlayerProgress
# Register your models here.
@admin.register(TreasureHuntGame)
class TreasureHuntGameAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "description", "start_time", "end_time", "is_active", )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("pk", "game", "order", "description", "answer", "hint", )


@admin.register(PlayerProgress)
class PlayerProgressAdmin(admin.ModelAdmin):
    list_display = ("pk", "player", "question", "is_completed", "completed_at", )
    