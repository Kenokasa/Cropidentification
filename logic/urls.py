from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import predict

urlpatterns = [
    path('diseases/', views.DiseaseListView.as_view(), name='disease-list'),
    path('save-snapshot/', views.save_snapshot, name='save-snapshot'),
    path('disease/<int:pk>/', views.DiseaseDetailView.as_view(), name='disease-detail'),
    path('scan/', views.scan_analysis_view, name='scan-analysis'),
    path('', views.robot_homepage, name='robot-homepage'),
    # path('pridi', views.
    path('file/<int:file_id>/', views.view_model, name='view-file'),
    path('predict/', predict, name='predict_leaf_disease'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
