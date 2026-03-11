from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password", "password2")

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") != cleaned.get("password2"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone", "department", "bio", "avatar")


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Current Password")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        value = self.cleaned_data["old_password"]
        if not self.user.check_password(value):
            raise forms.ValidationError("Current password is incorrect.")
        return value

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("new_password") != cleaned.get("new_password2"):
            raise forms.ValidationError("New passwords do not match.")
        return cleaned
