from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .models import Profile


class AccountSingIn(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the username'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the password'
            }
        )
    )

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            qs = User.objects.filter(username=username)
            if not qs.exists():
                raise forms.ValidationError(
                    f'User with this username {username} already exists')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Incorrect password')
            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError(
                    f'User {username} has been banned'
                )
        return super(AccountSingIn, self).clean(*args, **kwargs)


class AccountForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your the username'}))
    photo = forms.ImageField(required=False,
                             widget=forms.ClearableFileInput(
                                 attrs={'class': 'form-control'}
                             ))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your the first name'}))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your the last name'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(
                'A user with this username already exists!'
            )
        return username

    class Meta:
        model = Profile
        fields = ['username', 'photo', 'first_name', 'last_name']