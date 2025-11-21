from django import forms


class AuthForm(forms.Form):
    username = forms.CharField(
        required=True,
        label="Username",
        max_length=20,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter username"}
        ),
    )

    password = forms.CharField(
        max_length=20,
        label="Password",
        required=True,
        min_length=5,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter password"}
        ),
    )
