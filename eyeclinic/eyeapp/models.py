from django.db import models
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import path

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Appointment(BaseModel):
    FullName = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    PhoneNumber = models.CharField(max_length=200)
    service = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class AppointmentView(APIView):
        def get(self, request):
            appointments = Appointment.objects.all()
            serializer = AppointmentSerializer(appointments, many=True)
            return Response(serializer.data)

        def post(self, request):
            serializer = AppointmentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        def delete(self, request, pk):
            appointment = Appointment.objects.get(pk=pk)
            appointment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

urlpatterns = [
        path('appointments/', AppointmentView.as_view(), name='appointments'),
        path('appointments/<int:pk>/', AppointmentView.as_view(), name='appointment-detail'),
    ]
