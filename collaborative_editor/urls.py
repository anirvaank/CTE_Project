from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),  # Admin interface
    path("editor/", include("editor.urls")),  # Include editor app's URLs
]

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Welcome to the Collaborative Text Editor!")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("editor/", include("editor.urls")),  # Include editor app URLs
    path("", home_view, name="home"),  # Add this line for the root path
]
