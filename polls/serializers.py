from rest_framework import serializers
from .models import *


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'poll', 'choice', 'voted_by']
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'poll']

class PollSerializer(serializers.ModelSerializer):
    # per scrittura: lista di stringhe
    choices = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )

    # per lettura: nested serializer
    choices_data = ChoiceSerializer(source='choices', many=True, read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Poll
        fields = [
            'id',
            'question',
            'created_by',
            'created_at',
            'category',
            'choices',        # write-only
            'choices_data',   # read-only
            'created_by_username'  # read-only
        ]
        read_only_fields = ['created_by']

    def to_representation(self, instance):
        # usa la serializzazione di base
        rep = super().to_representation(instance)
        # rinomina choices_read → choices
        rep['choices'] = rep.pop('choices_data', [])
        return rep

    def create(self, validated_data):
        choices = validated_data.pop('choices', [])
        poll = Poll.objects.create(**validated_data)
        for choice in choices:
            Choice.objects.create(poll=poll, text=choice)
        return poll

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category  # Assuming you want to serialize Poll for categories
        fields = ['name']  # Adjust fields as necessary
        read_only_fields = ['name']