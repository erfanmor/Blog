from .models import Post


def get_recent_posts(request):
    recent_posts = Post.objects.order_by('-date')[:3]
    return {'recent_posts': recent_posts}
