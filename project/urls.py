from .views import RegisterView, LoginView, exam_qr_code, ExamViewSet, AnswerSheetAPIView
from django.urls import path



exam_list = ExamViewSet.as_view({
    'get': 'retrieve_by_code',
})

urlpatterns = [
    path('exams/by-code/<str:code>/', exam_list, name='exam-by-code'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('answer-sheet/', AnswerSheetAPIView.as_view(), name='login'),
    path('admin/exam/<int:exam_id>/qr/', exam_qr_code, name='exam_qr_code'),
]
