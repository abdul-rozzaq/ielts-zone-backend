from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import *


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
    list_filter = ['exam']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass
