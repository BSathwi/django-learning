import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import google.generativeai as genai
from .models import UploadedPDF, PDFSummary
from .serializers import PDFUploadSerializer

# Load environment variables from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class PDFUploadView(APIView):
    """
    API View for uploading PDFs, extracting text, and generating top 10 points using Gemini API.
    """
    def post(self, request):
        serializer = PDFUploadSerializer(data=request.data)
        if serializer.is_valid():
            # Save the uploaded PDF
            uploaded_pdf = serializer.save()

            # Extract text from the PDF
            pdf_reader = PdfReader(uploaded_pdf.file.path)
            extracted_text = ''
            for page in pdf_reader.pages:
                extracted_text += page.extract_text()

            uploaded_pdf.extracted_text = extracted_text
            uploaded_pdf.save()

            # Generate summary using Gemini API
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")

                response = model.generate_content(
                    f"Summarize the following text into 10 important points:\n{extracted_text}"
                )

                summary_text = response.text
                top_points = summary_text.split("\n")[:10] 

                PDFSummary.objects.create(
                    pdf=uploaded_pdf,
                    top_points="\n".join(top_points)
                )

                return Response({
                    "message": "PDF processed successfully!",
                    "top_points": top_points
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({
                    "error": f"Error during summarization: {str(e)}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
