from .views import RegisterView, LoginView, exam_qr_code

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from project.views import ExamViewSet


exam_list = ExamViewSet.as_view({
    'get': 'retrieve_by_code',
})

urlpatterns = [
    path('exams/by-code/<str:code>/', exam_list, name='exam-by-code'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin/exam/<int:exam_id>/qr/', exam_qr_code, name='exam_qr_code'),
]
