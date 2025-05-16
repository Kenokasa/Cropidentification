from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
# from .views import predict

urlpatterns = [
   path('', views.robot_homepage, name='home'),
path('viewer/<int:file_id>/', views.view_model, name='view_model'),
path('predict/hf/', views.predict_with_hf_model, name='predict_with_hf_model'),
path('snapshot/save/', views.save_snapshot, name='save_snapshot'),
path('diseases/', views.DiseaseListView.as_view(), name='disease_list'),
path('diseases/<pk>/', views.DiseaseDetailView.as_view(), name='disease_detail'),
path('scan/', views.scan_analysis_view, name='scan-analysis'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
