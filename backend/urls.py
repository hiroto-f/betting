import os
from django.contrib import admin
from django.urls import path, include

ADMIN_PATH = os.environ.get("ADMIN_PATH", "admin")

urlpatterns = [
    path(f"{ADMIN_PATH}/", admin.site.urls),
    path("api/", include("betting.urls")),
]
