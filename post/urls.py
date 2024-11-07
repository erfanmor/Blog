from django.urls import path
from .views import (HomeView,
                    AllPostsView,
                    AddNewPostView,
                    PostDetailView,
                    UpdatePostView,
                    DeletePostView,
                    CommentReplayView,
                    LikePostView,
                    PostsByTagView,
                    CategoriesView,
                    ProjectInfoView,
                    AboutMeView,)


urlpatterns = [
    # Home page
    path('', HomeView.as_view(), name='home'),

    # Posts URLs
    path('posts', AllPostsView.as_view(), name='all_posts'),
    path('posts/new', AddNewPostView.as_view(), name='add_post'),
    path('posts/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/replay', CommentReplayView.as_view(), name='replay_comment'),
    path('posts/update/<int:pk>', UpdatePostView.as_view(), name='update_post'),
    path('posts/delete/<int:pk>', DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/like/', LikePostView.as_view(), name='like_post'),

    # Categories URLs
    path('posts/caregory/<str:tag_name>/',
         PostsByTagView.as_view(), name='posts_by_tag'),
    path('posts/categories/', CategoriesView.as_view(), name='categories'),

    # About section
    path('project-info/', ProjectInfoView.as_view(), name='project_info'),
    path('about-me/', AboutMeView.as_view(), name='about_me'),
]
