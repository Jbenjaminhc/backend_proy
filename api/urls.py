from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from api.views import (
    AuthUserRegistrationView,
    AuthUserLoginView,
    LogoutView,
    AllAccessView,
    PremiumView,
    ClienteView,
    AdminView,
    UserViewSet
)
from api.business_logic.presentaciones.views import (
    GenerarPresentacionView,
    ListarPresentacionesView,
    DescargarPresentacionView,
    AgregarColaboradorView,
    ActualizarContenidoView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

#  Agrupación de autenticación bajo /auth/
auth_patterns = [
    path('signup', AuthUserRegistrationView.as_view(), name='signup'),
    path('signin', AuthUserLoginView.as_view(), name='signin'),
    path('signout', LogoutView.as_view(), name='signout'),
]

urlpatterns = [
    # JWT
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    #  rutas de autenticación agrupadas como /auth/*
    path('auth/', include((auth_patterns, 'auth'))),

    #  tests de acceso
    path('test/all', AllAccessView.as_view(), name='test_all'),
    path('test/premium', PremiumView.as_view(), name='test_premium'),
    path('test/cliente', ClienteView.as_view(), name='test_cliente'),
    path('test/admin', AdminView.as_view(), name='test_admin'),

    # Presentaciones
    path('presentaciones/generar/', GenerarPresentacionView.as_view(), name='generar_presentacion'),
    path('presentaciones/', ListarPresentacionesView.as_view(), name='listar_presentaciones'),
    path('presentaciones/descargar/<int:pk>/', DescargarPresentacionView.as_view(), name='descargar_presentacion'),
    path('presentaciones/<int:pk>/agregar-colaborador/', AgregarColaboradorView.as_view(), name='agregar_colaborador'),
    path('presentaciones/<int:pk>/guardar/', ActualizarContenidoView.as_view(), name='guardar_presentacion'),

    # Users
    path('', include(router.urls)),
]
