from django.utils.translation import ugettext_lazy as _
from django import forms
from .models import Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Blogger

class CommentModelForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['description']
        labels = { 'description': _('Description'), }
        help_texts = {'description': _('Enter comment about blog here.'), }

class SignUpForm(UserCreationForm):
    bio = forms.CharField(label="bio", widget=forms.Textarea, max_length=1000)

    class Meta:
        model = User
        fields = ('username', 'bio', 'password1', 'password2', )

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)

class BloggerForm(forms.ModelForm):
    class Meta:
        model = Blogger
        fields = ('bio',)