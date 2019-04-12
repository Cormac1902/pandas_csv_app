from django.urls import path
from . import views

urlpatterns = [
    path('', views.csv_upload, name='csv_upload'),
    path('validateCSV', views.check_csv, name='check_csv'),
]