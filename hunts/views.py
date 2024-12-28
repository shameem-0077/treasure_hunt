from django.utils import timezone
from core.functions import success_response_data, error_response_data, generate_serializer_errors, get_tokens_for_user
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.models import Player
from hunts.models import PlayerProgress, Question
from .serializers import GetUserQuestionSerializer, ValidateUserQuestionAnswer


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_user_question(request):
    player = Player.objects.get(user=request.user)
    current_player_progress = PlayerProgress.objects.get(player=player, question__order=player.current_question, is_completed=False)

    serializer = GetUserQuestionSerializer(instance=current_player_progress.question, context={"request": request}).data
    response_data = success_response_data(data=serializer, message="User question listed")
    return Response(response_data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="post",
    request_body=ValidateUserQuestionAnswer,
    operation_description="ValidateUserQuestionAnswer form",
    consumes=['application/x-www-form-urlencoded', 'multipart/form-data'],
)
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def validate_user_question(request):
    serializer = ValidateUserQuestionAnswer(data=request.data)
    if serializer.is_valid():
        player = Player.objects.get(user=request.user)
        current_player_progress = PlayerProgress.objects.get(player=player, question__order=player.current_question, is_completed=False)
        answer = serializer.validated_data.get("answer")

        if current_player_progress.question.answer == answer:
            current_player_progress.is_completed = True
            current_player_progress.completed_at = timezone.now()
            current_player_progress.save()
            response_data = success_response_data(message="Success")
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = error_response_data(errors={"answer": "Answer not correct"})
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    else:
        response_data = error_response_data(errors=generate_serializer_errors(serializer._errors), description="Validation error")
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

