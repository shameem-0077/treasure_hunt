from django.shortcuts import render
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
from hunts.models import PlayerProgress
from .serializers import GetUserQuestionSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_user_question(request):
    player = Player.objects.get(user=request.user)
    print(player, "player====")
    current_player_progress = PlayerProgress.objects.get(player=player, question__order=player.current_question, is_completed=False)

    serializer = GetUserQuestionSerializer(instance=current_player_progress.question, context={"request": request}).data
    response_data = success_response_data(data=serializer, message="User question listed")
    return Response(response_data, status=status.HTTP_200_OK)