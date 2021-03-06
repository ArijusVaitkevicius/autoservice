from .models import OrderComment
from .models import Profile
from django import forms
from django.contrib.auth.models import User


class OrderCommentForm(forms.ModelForm):
    class Meta:
        model = OrderComment
        fields = ['content', 'order', 'commentator']
        widgets = {'order': forms.HiddenInput(), 'commentator': forms.HiddenInput()}


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']
