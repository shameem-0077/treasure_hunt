import uuid

from django.utils.text import slugify
from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import Player
from hunts.models import TreasureHuntGame

from core.functions import get_tokens_for_user


class CreateAccountSerializer(serializers.Serializer):
    team_name = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()
    game_id = serializers.IntegerField(required=False)

    def validate(self, data):
        email = data.get("email")
        game_id = data.get("game_id", None)
        
        if User.objects.filter(username=email).exists():
            raise serializers.ValidationError({"account": "Already exists"})
        
        if game_id:
            game = TreasureHuntGame.objects.get(pk=game_id, is_active=True)
        else:
            game = TreasureHuntGame.objects.filter(is_active=True).first()
        
        if not game:
            raise serializers.ValidationError({"game": "No game not found to add"})
        
        return data


    def create(self, validated_data):
        team_name = validated_data.get("team_name")
        email = validated_data.get("email")
        password = validated_data.get("password")
        game_id = validated_data.get("game_id", None)

        team_name = slugify(team_name)
        user = User.objects.create_user(
            first_name=team_name,
            username=email,
            email=email,
            password=password
        )

        if game_id:
            game = TreasureHuntGame.objects.get(pk=game_id, is_active=True)
        else:
            game = TreasureHuntGame.objects.filter(is_active=True).first()

        player = Player.objects.create(
            user=user,
            game=game,
        )

        data = {
            "team_name": user.first_name,
            "team_unique_id": player.unique_id,
            "tokens": get_tokens_for_user(user=user)
        }

        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField()