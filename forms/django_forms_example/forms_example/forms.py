from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class UserCreatingForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
            "is_staff",
            "gender",
            "photo",
            "birth_date",
            "country",
            "description",
        )

        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter first name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter last name"}
            ),
        }

    username = forms.CharField(
        required=True,
        label="Username",
        max_length=20,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter username"}
        ),
    )
    password1 = forms.CharField(
        max_length=20,
        label="Password",
        required=True,
        min_length=5,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter password"}
        ),
    )
    password2 = forms.CharField(
        max_length=20,
        label="Confirm password",
        required=True,
        min_length=5,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirmed entered password"}
        ),
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        max_length=60,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter email"}
        ),
    )
    is_staff = forms.BooleanField(
        label="Is staff member",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    gender = forms.ChoiceField(
        label="Gender",
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
        ],
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
    )
    photo = forms.ImageField(
        required=False,
        label="Profile photo",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
    )
    birth_date = forms.DateField(
        required=True,
        label="Date of birth",
        # widget=forms.DateInput(attrs={'type': 'date'})
        widget=forms.SelectDateWidget(
            years=range(1900, 2026),
            attrs={"class": "form-select date-select"},
        ),
    )
    country = forms.ChoiceField(
        label="Country",
        choices=[
            ("Ukraine", "Ukraine"),
            ("Germany", "Germany"),
            ("Slovakia", "Slovakia"),
            ("Poland", "Poland"),
            ("USA", "USA"),
            ("Italy", "Italy"),
        ],
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    description = forms.CharField(
        required=False,
        label="Description",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Tell us about yourself...",
            }
        ),
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match.")

        return password2

    def save(self, commit: bool = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user


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
