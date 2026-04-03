FROM python:3.13-alpine

ENV PYTHONUNBUFFERED=1 
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apk update && \
    apk add --update --no-cache \
    build-base linux-headers

ARG user=django-user

RUN adduser $user --disabled-password

RUN mkdir -p /app /app/static && \
    chown -R $user /app /app/static

ADD ./requirements.txt ./requirements.txt

USER $user

ENV PATH="/home/$user/.local/bin:/usr/bin:$PATH"

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]