from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(r"download_report",
         views.download_report, name="download_report")
]
