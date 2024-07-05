from rest_framework import serializers

from project.models import Answer, Exam, Pupil, Test


class PupilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pupil
        fields = ('id', 'full_name')

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'text')

class TestSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Test
        fields = ('id', 'question', 'answers')

class ExamSerializer(serializers.ModelSerializer):
    tests = TestSerializer(many=True)

    class Meta:
        model = Exam
        fields = ('title', 'id', 'code', 'duration', 'tests')
