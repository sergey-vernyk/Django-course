from email.mime.image import MIMEImage

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import BadHeaderError, EmailMessage, send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .forms import FeedbackForm


def feedback_extend_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]
            attachment: InMemoryUploadedFile | None = form.cleaned_data.get(
                "attachment"
            )

            try:
                email_message = EmailMessage(
                    subject="Дякуємо за ваш відгук!",
                    body=render_to_string(
                        "mailing/email.html", context={"message": message}
                    ),
                    from_email=None,
                    to=[settings.ADMIN_EMAIL],
                    headers={"Reply-To": email},
                    cc=["kopohef433@emaxasp.com"],
                    bcc=["olive8612@airsworld.net"],
                )

                if attachment is not None:
                    email_message.attach(
                        filename=attachment.name,
                        content=attachment.file.read(),
                        mimetype=attachment.content_type,
                    )

                logo = finders.find("images/GoiTeens_logo.png")
                if logo is not None and isinstance(logo, str):
                    with open(logo, "rb") as f:
                        logo = MIMEImage(f.read())
                        # Content-ID використовується для вставки зображення в HTML:
                        # <img src="cid:logo">
                        logo.add_header("Content-ID", "<logo>")
                        # це inline-зображення
                        # (деякі поштові клієнти все одно можуть показувати його як вкладення)
                        logo.add_header(
                            "Content-Disposition", "inline", filename="logo.png"
                        )
                        email_message.attach(logo)

                email_message.content_subtype = "html"
                email_message.send(fail_silently=False)
            except BadHeaderError:
                return HttpResponse("Invalid header found.", status=400)

            return HttpResponse("<h2>Thanks for your feedback!</h2>")

    else:
        form = FeedbackForm()

    return render(request, "mailing/feedback.html", context={"form": form})


def feedback_view(request: HttpRequest) -> HttpResponse:
    """Просте відправлення email."""
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            try:
                send_mail(
                    subject="Ви залишили відгук",
                    message=message,
                    from_email=None,
                    recipient_list=[email, settings.ADMIN_EMAIL],
                    html_message=f"<p>{message}</p>",
                )
            except BadHeaderError:
                return HttpResponse("Invalid header found.", status=400)

            return HttpResponse("<h2>Thanks for your feedback!</h2>")

    else:
        form = FeedbackForm()

    return render(request, "mailing/feedback.html", context={"form": form})
