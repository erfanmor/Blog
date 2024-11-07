from django.views.generic.edit import CreateView
from django.views.generic import DetailView, View
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, ChangeProfileForm, ChangeSocialMediaForm
from .models import CustomUser
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from post.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ProfileView(DetailView):
    model = CustomUser
    template_name = 'account/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user


class ChangeUserProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile_form = ChangeProfileForm(instance=request.user)
        social_media_form = ChangeSocialMediaForm(instance=request.user)
        form = request.GET.get('form', 'default')

        context = {
            'form': form
        }

        if form == 'info':
            context['profile_form'] = profile_form
            return render(request, 'account/change_profile.html', context)

        elif form == 'social_media':
            context['social_media_form'] = social_media_form
            return render(request, 'account/change_profile.html', context)

        else:
            return redirect('profile')

    def post(self, request, *args, **kwargs):
        profile_form = ChangeProfileForm(
            request.POST, request.FILES, instance=request.user)
        social_media_form = ChangeSocialMediaForm(
            request.POST, instance=request.user)
        
        # Check form variable and send it special form to context
        form = request.POST.get('form', 'default')

        if 'profile_form' in request.POST and profile_form.is_valid():
            profile_form.save()
            return redirect('profile')

        if 'social_media_form' in request.POST and social_media_form.is_valid():
            social_media_form.save()
            return redirect('profile')

        context = {
            'form': form,
            'profile_form': profile_form,
            'social_media_form': social_media_form,
        }
        return render(request, 'account/change_profile.html', context)


class UserProfileDetailView(DetailView):
    model = CustomUser
    template_name = 'account/user_profile_detail.html'
    context_object_name = 'userprofile'

    def get_object(self):
        username = self.kwargs.get('username')
        return get_object_or_404(CustomUser, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return CustomUser.object.filter(is_active=True)
