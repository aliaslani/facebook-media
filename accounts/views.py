from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import CreateView, FormView, DetailView
from accounts.forms import RegisterForm, SocialLinkForm, UserUpdateForm
from accounts.models import CustomUser, SocialLink
from extra_views import UpdateWithInlinesView, InlineFormSetFactory, CreateWithInlinesView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


class SocialLinkInline(InlineFormSetFactory):
    model = SocialLink
    form_class = SocialLinkForm
    factory_kwargs = {
        'extra': 1,
        'max_num': 1,
        'can_delete': True,
    }


class RegisterView(CreateWithInlinesView):
    model = CustomUser
    form_class = RegisterForm
    inlines = [SocialLinkInline]
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('post_table')

class ProfileView(DetailView):
    model = CustomUser
    template_name = 'accounts/profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['social_links'] = SocialLink.objects.filter(user=self.object)
        return context

class ProfileUpdateView(UpdateWithInlinesView):
    model = CustomUser
    form_class = UserUpdateForm
    inlines = [SocialLinkInline]
    template_name = 'accounts/profile_update.html'
    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})




class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('post_table')


    def get_success_url(self):
        return self.success_url
    
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')
