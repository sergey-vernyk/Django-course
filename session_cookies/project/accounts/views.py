from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def password_reset_request(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.filter(email=email).first()

            if user is not None:
                context = {
                    "email": email,
                    "domain": "127.0.0.1:8000",
                    "site_name": "Website",
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user_username": user.get_username(),
                    "token": default_token_generator.make_token(user),
                    "protocol": "http",
                }

                form.send_mail(
                    subject_template_name="accounts/registration/password_reset_subject.txt",
                    email_template_name="accounts/registration/password_reset_email.txt",
                    context=context,
                    from_email="admin@mysite.com",
                    to_email=user.email,
                    html_email_template_name="accounts/registration/password_reset_email.html",
                )

                return redirect(reverse("password_reset_done"))
    else:
        form = PasswordResetForm()

    return render(
        request,
        template_name="accounts/registration/password_reset.html",
        context={"password_reset_form": form},
    )
