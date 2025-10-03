from django.urls import path
from . import views
urlpatterns = [
    path('upload/',views.upload_file,name='upload'),
    path('files/',views.file_list,name='file_list'),
]

