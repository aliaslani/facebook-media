import os
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.views.generic import CreateView, FormView, DetailView, TemplateView, ListView
from django_tables2 import SingleTableMixin

from accounts.forms import RegisterForm, SocialLinkForm, UserUpdateForm, ContactForm1, ContactForm2
from accounts.models import CustomUser, SocialLink, Contact
from extra_views import UpdateWithInlinesView, InlineFormSetFactory, CreateWithInlinesView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django_otp.plugins.otp_totp.models import TOTPDevice
import qrcode
from django.db import transaction

from core.tables import ContactTable
from core.tasks import send_welcome_email
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from django_filters.views import FilterView
from core.filters import ContactFilter

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



class ContactWizardView(SessionWizardView):
    form_list = [
        ('first', ContactForm1),
        ('second', ContactForm2),
    ]
    TEMPLATES = {
        'first': 'accounts/contact_form1.html',
        'second': 'accounts/contact_form1.html',
    }
    file_storage = FileSystemStorage(os.path.join(settings.MEDIA_ROOT, 'temp_uploads'))
    def get_template_names(self):
        return [self.TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)

        contact = Contact.objects.create(
            subject=data['subject'],
            sender=data['sender'],
            message=data['message'],
            file=data['file'],
        )


        return redirect('contact_list')

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context.update({
            'current_step_name': self.steps.current,
            'total_steps': len(self.form_list),
            'current_step_number': list(self.form_list).index(self.steps.current) + 1,
            'progress_percentage': (
                    (list(self.form_list).index(self.steps.current) + 1)
                    * 100
                    / len(self.form_list)
            )
        })
        return context


class ContactListView(SingleTableMixin, FilterView):
    model = Contact
    template_name = 'accounts/contact_list.html'
    filterset_class = ContactFilter
    context_object_name = 'contacts'
    table_class = ContactTable
    paginate_by = 5