from rest_framework import serializers
from question.models import Questions,Options

class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Questions
        fields=(
            'question',
        )
class AddQuestionSerializer(serializers.Serializer):
    question=serializers.CharField()

class AddOptionSerializer(serializers.Serializer):
    options=serializers.CharField()

class OptionSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
   
    class Meta:
        model=Options
        fields=(
            'id',
            'options',
            'question'
           
        )
    # def to_representation(self, obj):
    #   return  obj.options , obj.id

    def get_question(self, instance):
        if instance.question:
            return instance.question.question
        else:
            return None
        
class ListOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Options
        fields=(
            'id',
            'options',
        )
    
    




   

    
        
    
