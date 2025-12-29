from django import forms


class FeedbackForm(forms.Form):
    email = forms.EmailField(
        max_length=60,
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter your email"}
        ),
    )

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Enter your feedback",
                "required": True,
            }
        )
    )
