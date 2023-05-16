from django.shortcuts import render
from django.http import HttpResponse

def upload_view(request):
    return render(request, 'upload.html')

def download_view(request):
    return render(request, 'download.html')