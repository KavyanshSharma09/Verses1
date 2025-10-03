from django.shortcuts import render,redirect
from .models import UploadFile

def upload_file(request):
    if request.method == "POST":
        uploaded_file = request.FILES["file"]
        UploadFile.objects.create(file=uploaded_file)
        return redirect("file_list")
    return render(request,"upload/upload.html")

def file_list(request):
    files = UploadFile.objects.all().order_by("-uploaded_at")
    return render(request, "upload/file_list.html", {"files": files})
