from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderViewSet.as_view({'get': 'list'})),
    path('checkout/', views.OrderViewSet.as_view({'post': 'checkout'})),
]