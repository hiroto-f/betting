# betting/serializers.py
from rest_framework import serializers
from .models import Event, Option, Bet


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "event", "name"]


class EventSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ["id", "title", "created_at", "options"]


class BetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
        fields = ["id", "option", "username", "amount", "created_at"]