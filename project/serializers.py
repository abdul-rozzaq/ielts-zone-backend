from rest_framework import serializers

from project.models import Answer, Exam, Pupil, PupilAnswer, Test, AnswerSheet


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



class PupilAnswerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PupilAnswer
        exclude = ['answer_sheet', 'is_correct']


class AnswerSheetSerializer(serializers.ModelSerializer):
    answers = PupilAnswerSerializer(many=True, write_only=True)

    class Meta:
        model = AnswerSheet
        fields = ('pupil', 'exam', 'answers')
        
        
    def create(self, validated_data):
        data = {**validated_data}
        answers = data.pop('answers')
        obj = super().create(data)
        
        for ans in answers:
            PupilAnswer.objects.create(**ans, answer_sheet=obj)
        
        return obj