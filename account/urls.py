from django.urls import path
from .views import SignUpView, ProfileView, ChangeUserProfileView, UserProfileDetailView


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change/profile/', ChangeUserProfileView.as_view(), name='change_profile'),
    path('profile/<str:username>', UserProfileDetailView.as_view(), name='user_profile'),
]
