from django.urls import path
from accounts.views import RegisterView, ProfileUpdateView, ProfileView, CustomLoginView, CustomLogoutView, login_view, \
    ContactWizardView, ContactListView
from accounts.forms import ContactForm1, ContactForm2
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('login-otp/', login_view, name='login_otp'),
    path('contact/', ContactWizardView.as_view(), name='contact'),
    path('contact-list/', ContactListView.as_view(), name='contact_list'),
]