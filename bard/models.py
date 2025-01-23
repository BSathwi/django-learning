from django.db import models

class UploadedPDF(models.Model):
    file = models.FileField(upload_to='uploads/')
    extracted_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PDF {self.id} - {self.file.name}"


class PDFSummary(models.Model):
    pdf = models.OneToOneField(UploadedPDF, on_delete=models.CASCADE, related_name='summary')
    top_points = models.TextField()

    def __str__(self):
        return f"Summary for PDF {self.pdf.id}"
