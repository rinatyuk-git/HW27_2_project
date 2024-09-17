from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView)

from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter

from users.views import (
    # UserViewSet,
    UserCreateAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
    UserDestroyAPIView,
    PaymentsListAPIView,
    )

app_name = UsersConfig.name

# router = DefaultRouter()
# router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    path('users/create/', UserCreateAPIView.as_view(), name='user_create'),
    path('users/', UserListAPIView.as_view(), name='user_list'),
    path('users/<int:pk>', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('users/update/<int:pk>', UserUpdateAPIView.as_view(), name='user_update'),
    path('users/delete/<int:pk>', UserDestroyAPIView.as_view(), name='user_delete'),
    path('users/login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('users/token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('payments/', PaymentsListAPIView.as_view(), name='payments_list'),
]

# urlpatterns += router.urls
