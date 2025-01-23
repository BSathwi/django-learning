from rest_framework import serializers
from .models import UploadedPDF

class PDFUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedPDF
        fields = ['file']
