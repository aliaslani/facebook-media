from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.views.generic import CreateView, FormView, DetailView, TemplateView
from accounts.forms import RegisterForm, SocialLinkForm, UserUpdateForm
from accounts.models import CustomUser, SocialLink
from extra_views import UpdateWithInlinesView, InlineFormSetFactory, CreateWithInlinesView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django_otp.plugins.otp_totp.models import TOTPDevice
import qrcode
from django.db import transaction
from core.tasks import send_welcome_email


from PIL.Image import Image
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

    def forms_valid(self, form, inlines):
        response = super().forms_valid(form, inlines)

        user_email = self.object.email

        transaction.on_commit(
            lambda: send_welcome_email(user_email)
        )

        return response



class ProfileView(DetailView):
    model = CustomUser
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    queryset = CustomUser.objects.prefetch_related(
        "social_links",
        "posts",
    )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['social_links'] = SocialLink.objects.filter(user=self.object)
        context["is_owner"] = (
            self.request.user.is_authenticated
            and self.request.user.id == self.object
        )
        return context

    def get_object(self, queryset=None):
        user = self.request.user
        return user

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

def login_view(request):
    device = TOTPDevice.objects.create(
        user=request.user,
        name='my phone',
        confirmed=True,
    )
    config_url = device.config_url
    image = qrcode.make(config_url)

    if request.method == 'POST':
        pass
    return render(request, 'accounts/otp_login.html', {'device': device, 'config_url': config_url, 'img': image})



    def get_success_url(self):
        return self.success_url
    
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

