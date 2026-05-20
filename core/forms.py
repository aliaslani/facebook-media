from django.forms import Form, ModelForm
from django import forms
from core.models import Post, TaggedUser, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Submit, Layout, Field

class NewPostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        # self.helper.layout = Layout(
        #     'title',
        #     'content',
        #     'subject',
        # )
        # self.helper.field_class = 'mb-3'
        # self.helper.label_class = 'form-label'
        # self.helper.layout = Layout(
        #     Field('title', css_class='form-control', placeholder='Title...'),
        #     Field('content', css_class='form-control', placeholder='Content...', rows=4),
        #     Field('subject', css_class='form-select'),
        # )
        self.helper.layout = Layout(
            Fieldset(
                "New Post",
                'title',
                'content',
                'subject',
            ),
            # Submit('submit', 'Submit', css_class='btn btn-primary')
            )

    class Meta:
        model = Post
        fields = ['title', 'content', 'subject']


        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'title...'},),
            'content': forms.Textarea(attrs={'class':'form-control', 'cols':30, 'rows':4}),
            'subject': forms.Select(attrs={'class':'form-select'}),
        }
        

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError('Title must be at least 5 characters long.')
        return title
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise forms.ValidationError('Content must be at least 10 characters long.')
        return content
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title and content:
            if title in content:
                raise forms.ValidationError('Content should not contain the title.')
        return cleaned_data



class TaggedUserForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, kwargs)
        self.helper = FormHelper()
        self.helper.form_tag= False
    class Meta:
        model = TaggedUser
        fields = ['user']


class CommentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, kwargs)
        self.helper = FormHelper()
        self.helper.form_tag= False
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control', 'cols':30, 'rows':4}),
        }