from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('document/<int:pk>/', views.DocumentDetailView.as_view(), name='document_detail'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('process/<int:pk>/', views.ProcessDocumentView.as_view(), name='process_document'),
    path('download/<int:pk>/<str:format>/', views.DownloadView.as_view(), name='download'),
]
