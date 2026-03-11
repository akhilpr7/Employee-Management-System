from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View

from .forms import RegisterForm, ProfileForm, ChangePasswordForm

class LoginView(View):
    template_name = "accounts/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("employees:list")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = AuthenticationForm(request)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(request.GET.get("next", "employees:list"))
        return render(request, self.template_name, {"form": form})


class RegisterView(View):
    template_name = "accounts/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("employees:list")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully. Welcome!")
            return redirect("employees:list")
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("accounts:login")


class ProfileView(LoginRequiredMixin, View):
    template_name = "accounts/profile.html"

    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")
        return render(request, self.template_name, {"form": form})


class ChangePasswordView(LoginRequiredMixin, View):
    template_name = "accounts/change_password.html"

    def get(self, request):
        form = ChangePasswordForm(request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data["new_password"])
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Password changed successfully.")
            return redirect("accounts:profile")
        return render(request, self.template_name, {"form": form})
