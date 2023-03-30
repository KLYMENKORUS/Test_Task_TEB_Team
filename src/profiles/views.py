from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView, UpdateView, DeleteView
from .forms import AccountSingIn, AccountForm
from .models import Profile


def index(request):
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = None
    return render(request, 'profiles/index.html', {'user_id': user_id})


class SignInView(FormView):
    form_class = AccountSingIn
    template_name = 'profiles/sign_in.html'
    success_url = reverse_lazy('profiles:index')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        messages.success(
            self.request,
            f'Hi {self.request.POST["username"]}')
        return super().form_valid(form)


class AccountLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'profiles/index.html'

    def get_success_url(self):
        messages.success(self.request, 'You have successfully logged out')
        return reverse_lazy('profiles:index')


class AccountDetailView(LoginRequiredMixin, DetailView, FormView):
    model = Profile
    form_class = AccountForm
    template_name = 'profiles/detail.html'

    def get_form_kwargs(self):
        kwargs = super(AccountDetailView, self).get_form_kwargs()
        kwargs['initial'] = {
            'username': self.object.username,
            'first_name': self.object.first_name,
            'last_name': self.object.last_name,
            'photo': self.object.photo
        }
        return kwargs


class AccountUpdateView(UpdateView):
    model = Profile
    template_name = 'profiles/detail.html'
    form_class = AccountForm

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy(
            'profiles:detail', kwargs={'pk': self.object.pk}
        )

    def form_valid(self, form):
        profile_form = form.save(commit=False)
        profile_form.user = self.request.user
        profile_form.save()
        messages.success(self.request, 'Profile updated successfully')
        return super().form_valid(form)


class DeleteProfileView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('profiles:index')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request,
                         'Profile deleted successfully')
        return redirect(self.success_url)


