from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()


class RegisterForm(forms.Form):
    email = forms.EmailField()
    full_name = forms.CharField()
    password = forms.CharField()
    confirm_password = forms.CharField()
    is_doctor = forms.BooleanField(required=False)