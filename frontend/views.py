from django.shortcuts import render
from django.http import HttpResponse
from frontend.endpoints import BACKENDS
import requests
import random
import json
from django.shortcuts import redirect
import time
from django.contrib import messages

def upload_view(request):
    if request.method == 'GET':
        return render(request, 'upload.html')
    elif request.method == 'POST':
        selected_backend = select_backend()
        print(selected_backend)
        if selected_backend:
            uploaded_file = request.FILES['file']
            file_id = request.POST['id']
            response = requests.post(selected_backend + f'/storage/upload-file?file_id={file_id}', files={'file': uploaded_file})
            for i in range(60):
                time.sleep(1)
                requests.get(selected_backend + f'/storage/get-file/{file_id}')
                if response.status_code == 200:
                    messages.success(request, 'File uploaded successfully')
                    return redirect('/download')
            return render(request, 'upload.html', {'error': 'File upload failed'})
        return HttpResponse('Service Unavailable', status=503)

def download_view(request):
    selected_backend = select_backend()
    print(selected_backend)
    if selected_backend:
        context = {}
        response = requests.get(selected_backend + '/storage/get-file')
        if response.status_code == 200:
            response_data = json.loads(response.text)
            files = response_data['data']
            context['files'] = files
            context['selected_backend'] = selected_backend
            print(files)
        return render(request, 'download.html', context)
    return HttpResponse('Service Unavailable', status=503)

def download_file(request, id):
    selected_backend = select_backend()
    print(selected_backend)
    if selected_backend:
        return redirect(selected_backend + '/storage/get-file/' + id)
    return HttpResponse('Service Unavailable', status=503)

def select_backend():
    backends = BACKENDS[:]
    while backends:
        backend_url = random.choice(backends)
        try:
            response = requests.options(backend_url + '/storage/get-file')
            print(response.status_code)
            if response.status_code == 200:
                return backend_url
        except requests.exceptions.RequestException:
            pass
        backends.remove(backend_url)
    return None
