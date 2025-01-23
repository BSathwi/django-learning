from django.contrib import admin
from .models import UploadedPDF,PDFSummary
# Register your models here.
admin.site.register(PDFSummary)
admin.site.register(UploadedPDF)