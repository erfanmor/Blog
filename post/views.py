from django.views.generic import TemplateView, CreateView, ListView, DetailView, FormView
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Post, Likes, Tag
from .forms import AddNewPostForm, CommentForm, CommentReplayForm
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(TemplateView):
    template_name = 'home.html'


@method_decorator(login_required, name='dispatch')
class AllPostsView(View, LoginRequiredMixin):
    model = Post
    template_name = 'post/all_posts.html'
    login_url = '/account/login'
    paginate_by = 3

    def get(self, request):
        posts = Post.objects.all()

        # Paginator section
        paginator = Paginator(posts, self.paginate_by)
        page_nubmer = request.GET.get('page')
        page_obj = paginator.get_page(page_nubmer)
        paginator = Paginator(posts, self.paginate_by)

        count = paginator.count
        one_to_last = count - 1

        context = {
            'post_list': page_obj,
            'one_to_last': one_to_last,
        }

        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class AddNewPostView(CreateView):
    model = Post
    template_name = 'post/add_post.html'
    form_class = AddNewPostForm
    success_url = reverse_lazy('home')
    login_url = '/login/'

    def form_valid(self, form):
        # append author to post and save
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class UpdatePostView(UpdateView):
    model = Post
    template_name = 'post/update_post.html'
    fields = ['title', 'content', 'tags', 'photo']

    def get_object(self, queryset=None):
        
        # get post from pk in URL
        post = get_object_or_404(Post, pk=self.kwargs['pk'])

        # Check if user is author or not
        if post.author != self.request.user:
            raise PermissionDenied
        
        return post


@method_decorator(login_required, name='dispatch')
class DeletePostView(DeleteView):
    model = Post
    template_name = 'post/delete_post.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        
        # get post from pk in URL
        post = get_object_or_404(Post, pk=self.kwargs['pk'])

        # Check if user is author or not
        if post.author != self.request.user:
            raise PermissionDenied
        
        return post


@method_decorator(login_required, name='dispatch')
class PostDetailView(View):

    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


class CommentGet(DetailView):
    model = Post
    template_name = 'post/post_detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Increase view count
        if not request.COOKIES.get(f'viewed_post_{self.object.id}'):
            self.object.view_count += 1
            self.object.save()

            # Set seen Cookie
            response = super().get(request, *args, **kwargs)
           # Cookie for one hour
            response.set_cookie(
                f'viewed_post_{self.object.id}', 'true', max_age=3600)
            return response
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class CommentPost(SingleObjectMixin, FormView):
    model = Post
    form_class = CommentForm
    template_name = 'post/post_detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        post = self.get_object()
        return reverse('post_detail', kwargs={'pk': post.pk})


class CommentReplayView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('all_posts'))

    def post(self, request, *args, **kwargs):
        view = CommentReplayPost.as_view()
        return view(request, *args, **kwargs)


class CommentReplayPost(SingleObjectMixin, FormView):
    model = Post
    form_class = CommentReplayForm
    template_name = 'post/post_detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    # Validate and filling fields
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        post = self.get_object()
        return reverse('post_detail', kwargs={'pk': post.pk})


class LikePostView(View):
    def post(self, request, pk, *arks, **kwrags):
        post = get_object_or_404(Post, id=pk)

        if not request.user.is_authenticated:
            return HttpResponse("لطفاً وارد حساب کاربری خود شوید.", status=403)

        like, created = Likes.objects.get_or_create(
            user=request.user, post=post)

        if not created:
            like = Likes.objects.filter(user=request.user, post=post).first()
            if like:
                like.delete()

        likes_count = post.likes.count()
        likers = post.get_likers()

        data = {
            'likes_count': likes_count,
        }

        # User liked or not
        if str(request.user) in likers:
            data['user_liked'] = True
        else:
            data['user_liked'] = False

        return JsonResponse(data)


@method_decorator(login_required, name='dispatch')
class PostsByTagView(ListView):
    model = Post
    template_name = 'post/posts_by_tag.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get(self, request, tag_name):

        tag_name = tag_name
        tag = get_object_or_404(Tag, name=tag_name)
        posts = Post.objects.filter(tags=tag)

        # Paginator section
        paginator = Paginator(posts, self.paginate_by)
        page_nubmer = request.GET.get('page')
        page_obj = paginator.get_page(page_nubmer)

        count = paginator.count
        one_to_last = count - 1

        context = {
            'post_list': page_obj,
            'one_to_last': one_to_last,
            'tag': tag_name,
        }

        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class CategoriesView(ListView):
    model = Tag
    template_name = 'post/categories.html'


class ProjectInfoView(TemplateView):
    template_name = 'about/project.html'


class AboutMeView(TemplateView):
    template_name = 'about/me.html'
