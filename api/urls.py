from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt import views as jwt_views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import CreateUserApiView, UserPostListApiView, AllUsersApiView, UserInfoApiView


urlpatterns = [
    # Schema and Swagger
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),

    # JWT Authorization
    path('jwt-token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt-token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # Token Authorization
    path('get-token/', obtain_auth_token, name='api-generate-token'),

    # APIs
    path('create-user/', CreateUserApiView.as_view(), name='api-create-user'),
    path('users/', AllUsersApiView.as_view(), name='api-all-users'),
    path('user-posts/<str:username>', UserPostListApiView.as_view(), name='api-user-posts'),
    path('user-info/<str:username>', UserInfoApiView.as_view(), name='api-user-info'),
]
