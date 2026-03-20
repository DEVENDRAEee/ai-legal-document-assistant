from django.urls import path
from . import views

app_name = 'legal_analysis'

urlpatterns = [
    path('api/search/', views.SearchAPIView.as_view(), name='search_api'),
]




