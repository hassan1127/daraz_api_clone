from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views



from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Auth
    path('auth/register/', views.UserRegisterView.as_view()),
    path('auth/admin/register/', views.AdminRegisterView.as_view()),
    path('auth/login/', TokenObtainPairView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),

    # Profile
    path('me/', views.MeView.as_view()),

    # Seller flow
    path('seller/request/', views.SellerRequestView.as_view()),

    # Admin — renamed to dashboard/ to avoid conflict with Django admin
    path('dashboard/users/', views.AdminUserListView.as_view()),
    path('dashboard/seller-requests/', views.PendingSellerRequestsView.as_view()),
    path('dashboard/seller-requests/<int:user_id>/action/', views.SellerRequestActionView.as_view()),
]

'''urlpatterns = [
    # Auth
    path('auth/register/', views.UserRegisterView.as_view()),         # public
    path('auth/admin/register/', views.AdminRegisterView.as_view()),  # admin only
    path('auth/login/', TokenObtainPairView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),

    # Profile
    path('me/', views.MeView.as_view()),

    # Seller flow
    path('seller/request/', views.SellerRequestView.as_view()),

    # Admin
    path('admin/users/', views.AdminUserListView.as_view()),
    path('admin/seller-requests/', views.PendingSellerRequestsView.as_view()),
    path('admin/seller-requests/<int:user_id>/action/', views.SellerRequestActionView.as_view()),
]'''