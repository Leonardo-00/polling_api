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

class ChoiceUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)  # For existing choices
    new = serializers.BooleanField(default=False, write_only=True)
    delete = serializers.BooleanField(default=False, write_only=True)
    class Meta:
        model = Choice
        fields = ['id', 'text', 'new', 'delete']


class PollSerializer(serializers.ModelSerializer):
    # per scrittura: lista di stringhe
    choices = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )
    
    # per aggiornamento: lista di ChoiceUpdateSerializer
    choices_update = ChoiceUpdateSerializer(many = True, write_only=True, required=False)

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
            'choices_update',  # write-only, for updating choices
            'created_by_username'  # read-only
            
        ]
        read_only_fields = ['id', 'created_by', 'created_at']

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
    
    def update(self, instance, validated_data):
        choices_data = validated_data.pop('choices_update', [])

        poll = super().update(instance, validated_data)

        # aggiorna le choices
        for choice in choices_data:
            choice_id = choice.get('id')
            text = choice.get('text')
            try:
                if choice.get('new'):
                    # Se 'new' è True, crea una nuova scelta
                    Choice.objects.create(poll=poll, text=text)
                elif choice.get('delete'):
                    # Se 'delete' è True, elimina la scelta
                    Choice.objects.filter(id=choice_id, poll=poll).delete()
                else:
                    # Altrimenti, aggiorna il testo della scelta esistente
                
                    Choice.objects.filter(id=choice_id, poll=poll).update(text=text)
                    Vote.objects.filter(choice__id=choice_id, poll=poll).delete()  # Elimina i voti associati alla scelta aggiornata
            except Choice.DoesNotExist:
                pass  # oppure solleva errore se preferisci

        return instance

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category  # Assuming you want to serialize Poll for categories
        fields = ['name']  # Adjust fields as necessary
        read_only_fields = ['name']
        
