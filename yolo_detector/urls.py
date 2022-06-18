from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='yolo_detector_home'),
    path('detect/', views.detect_view, name='yolo_detector_detect'),
]
