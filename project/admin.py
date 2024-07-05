from typing import Any

from django.contrib import admin
from django.db.models import Case, Count, F, IntegerField, When
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html

from .models import *
from .filters import HighPercentageFilter

DANGER = '#DC3545'
SUCCESS = '#28A745'
WARNING = '#FFC107'

BAD = 40


@admin.register(Pupil)
class PupilAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'id', 'password')
    search_fields = ('full_name',)
     
    def get_fieldsets(self, request, obj=None):
        if obj:
            return [
                ['', {
                    'fields': ['full_name', 'password']
                }]
            ]
        else:
            return [
                ['', {
                    'fields': ['full_name']
                }]
            ]

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['key', 'pupil', 'created']

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

class TestInline(admin.TabularInline):
    model = Test
    extra = 1
    inlines = [AnswerInline]

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'duration', 'qr_code_button']
    
    def qr_code_button(self, obj):
        return format_html('<a class="button" href="{}">QR Kodini Ko\'rish</a>', reverse('exam_qr_code', args=[obj.id]))

    qr_code_button.short_description = 'QR Kod'
    qr_code_button.allow_tags = True

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ['question', 'get_correct_answer']
    list_filter = ['exam']
    
    def get_correct_answer(self, obj):
        correct_answer = obj.answers.filter(is_correct=True).first()
        return correct_answer.text if correct_answer else format_html('<a style="color: #fff; padding: 4px; background-color: {}; border-radius: 4px;">No correct answer</a)>', DANGER)
    
    get_correct_answer.short_description = 'Correct Answer'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'test', 'is_correct']
    list_filter = ['test__exam']


class PupilAnswerInline(admin.TabularInline):
    model = PupilAnswer
    
    def get_extra(self, request, obj, **kwargs) -> int:        
        tests_count = obj.exam.tests.count()        
        return tests_count - len([ x for x in obj.answers.all()])
        


@admin.register(AnswerSheet)
class AnswerSheetAdmin(admin.ModelAdmin):
    inlines = [PupilAnswerInline]
    list_display = ['pupil', 'exam', 'created', 'percentage', 'result']
    list_filter = ['exam', 'pupil', HighPercentageFilter]
    actions = ['clone']
    
    def percentage(self, obj: AnswerSheet):        
        tests_count = obj.exam.tests.count()
        correct_answers_count = len([ x for x in obj.answers.all() if x.is_correct ])
        
        percent = correct_answers_count /  tests_count * 100
        
        color = SUCCESS if percent >= 80 else WARNING if percent >= 60 else DANGER
        textColor = 'fff' if color != WARNING else '000'
        
        return format_html('<a style="color: #{}; padding: 4px 8px; font-weight: bold; background-color: {}; border-radius: 4px;">{}%</a)>', textColor, color, int(percent))
        
    percentage.admin_order_field = 'computed_percentage'

    def result(self, obj):
        tests_count = obj.exam.tests.count()
        correct_answers_count = len([ x for x in obj.answers.all() if x.is_correct ])
        
        return f'{correct_answers_count} / {tests_count}'
    
    
    @admin.action(description='Clone answer sheets')
    def clone(modeladmin, request, queryset):
        for obj in queryset:
            old_pk = obj.pk
            
            obj.pk = None
            obj.save()
            
            for x in PupilAnswer.objects.filter(answer_sheet_id=old_pk):
                x.pk = None
                x.answer_sheet = obj
                x.save()
            
            
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            tests_count=Count('exam__tests'),   
            correct_answers_count=Count(Case(When(answers__is_correct=True, then=1), output_field=IntegerField()))
        ).annotate(
            computed_percentage=F('correct_answers_count') * 100.0 / F('tests_count')
        )
        return queryset


@admin.register(PupilAnswer)
class PupilAnswerAdmin(admin.ModelAdmin):
    pass