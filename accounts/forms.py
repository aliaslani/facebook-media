from django import forms
from accounts.models import CustomUser, SocialLink
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Submit, Layout, Field
from django.contrib.auth.hashers import make_password


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'bio', 'city', 'profile_picture', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username...'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email...'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone...'}),
            'bio': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Bio...', 'rows':4}),
            'city': forms.TextInput(attrs={'class':'form-control', 'placeholder':'City...'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password...'}),
            'confirm_password': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password...'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Register",
                'username',
                'email',
                'phone',
                'bio',
                'city',
                'profile_picture',
                'password',
                'confirm_password',
            ),
            )
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        cleaned_data.pop('confirm_password', None)
        cleaned_data['password'] = make_password(cleaned_data['password'])
        return cleaned_data
    
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'bio', 'city', 'profile_picture']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username...'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email...'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone...'}),
            'bio': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Bio...', 'rows':4}),
            'city': forms.TextInput(attrs={'class':'form-control', '    placeholder':'City...'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class':'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Update Profile",
                'username',
                'email',
                'phone',
                'bio',
                'city',
                'profile_picture',
            ),
            )

class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ['platform', 'url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Social Link",
                'platform',
                'url',
            ),
            )
        