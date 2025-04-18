from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
#UserListView
from .views import (
    AuthUserRegistrationView,
    AuthUserLoginView,
    LogoutView,
    AllAccessView,
    PremiumView,
    ClienteView,
    AdminView,
    UserViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    #path('register', AuthUserRegistrationView.as_view(), name='register'),
    #path('login', AuthUserLoginView.as_view(), name='login'),
    #path('users', UserListView.as_view(), name='users')
    path('test/all', AllAccessView.as_view(), name='test_all'),
    path('test/premium', PremiumView.as_view(), name='test_premium'),
    path('test/cliente', ClienteView.as_view(), name='test_cliente'),
    path('test/admin', AdminView.as_view(), name='test_admin'),
    path('signin', AuthUserLoginView.as_view(), name='signin'),
    path('signup', AuthUserRegistrationView.as_view(), name='signup'),
    path('signout', LogoutView.as_view(), name='signout'),
    path('', include(router.urls)),
]
