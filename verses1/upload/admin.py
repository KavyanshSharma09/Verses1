from django.contrib import admin

from .models import UploadFile

class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('id','file','uploaded_at')
