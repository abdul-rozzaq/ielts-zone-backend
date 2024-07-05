from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import qrcode

from .models import Pupil, Token, Exam
from .authentication import TokenAuthentication
from .serializers import PupilSerializer, ExamSerializer



class RegisterView(APIView):

    def post(self, request):
        full_name = request.data.get('full_name')
        
        if not full_name:
            return Response({'error': 'Full name required'}, status=status.HTTP_400_BAD_REQUEST)

        pupil = Pupil(full_name=full_name, password='000000')
        pupil.save()
        
        token, created = Token.objects.get_or_create(pupil=pupil)
        
        return Response({**PupilSerializer(pupil).data,'token': str(token.key)}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        username = request.data.get('id')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Id and password required'}, status=status.HTTP_400_BAD_REQUEST)

        token = self.authentication_classes[0]().authenticate(request, username=username, password=password)
        
        if token:
            
            return Response({**PupilSerializer(token.pupil).data, 'token': str(token.key)}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

def exam_qr_code(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=25,
        border=2,
    )
    qr.add_data(exam.code)
    qr.make(fit=True)

    img = qr.make_image()

    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


class ExamViewSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['get'], url_path='by-code/(?P<code>[^/.]+)')
    def retrieve_by_code(self, request, code=None):
        exam = get_object_or_404(Exam, code=code)
        serializer = ExamSerializer(exam)
        return Response(serializer.data, status=status.HTTP_200_OK)