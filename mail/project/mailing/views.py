from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import FeedbackForm


def feedback_view(request: HttpRequest) -> HttpResponse:
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
