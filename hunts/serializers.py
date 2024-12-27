from rest_framework import serializers
from hunts.models import Question

class GetUserQuestionSerializer(serializers.ModelSerializer):
    is_last_question = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            "pk",
            "title",
            "description",
            "type",
            "attachment",
            "hint",
            "order",
            "is_last_question",
        )
    
    def get_is_last_question(self, obj):
        last_question = Question.objects.filter(game=obj.game).distinct().order_by('-order').first()

        if last_question == obj:
            return True
        return False


class ValidateUserQuestionAnswer(serializers.Serializer):
    answer = serializers.CharField()