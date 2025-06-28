from rest_framework import serializers
from .models import Poll, Choice, Vote

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'poll', 'text']

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'poll', 'choice', 'voted_by']

class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'question', 'created_by', 'created_at', 'choices']
        read_only_fields = ['created_by']
