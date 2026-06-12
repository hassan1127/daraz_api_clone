from django.urls import path
from . import views

cart_view = views.CartViewSet.as_view({
    'get': 'list',
})

urlpatterns = [
    path('', cart_view),
    path('add/', views.CartViewSet.as_view({'post': 'add_item'})),
    path('remove/', views.CartViewSet.as_view({'post': 'remove_item'})),
]