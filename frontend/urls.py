from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.upload_view, name='upload'),
    path('download', views.download_view, name='download'),
]
