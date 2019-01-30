from django import forms
from .models import Post, Comment, author
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'slug',
            'body',
            'image',
            'category',
            'tags',
        ]

class createAuthor(forms.ModelForm):
    class Meta:
        model = author
        fields =[
            'auth_image',
            'auth_details',
        ]


class CommentForm(forms.ModelForm):
    name    =   forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name*'}))
    email   =   forms.EmailField(label="", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your comments here!!!', 'cols':'30', 'rows':'10' }))
    class Meta:
        model = Comment
        fields = ('name','email','content')


class registerUser(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2'
        ]


