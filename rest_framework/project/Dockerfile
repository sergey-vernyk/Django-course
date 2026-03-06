# використовуємо легкий образ Python 3.13 на базі Alpine Linux
FROM python:3.13-alpine

# Python буде одразу виводити логи в консоль (важливо для Docker)
ENV PYTHONUNBUFFERED=1 

# забороняємо створення *.pyc файлів (щоб не засмічувати контейнер)
ENV PYTHONDONTWRITEBYTECODE=1

# встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# оновлюємо список пакетів і встановлюємо інструменти для збірки Python-залежностей
RUN apk update && \
    apk add --update --no-cache \
    build-base linux-headers

# ім'я користувача, під яким буде працювати застосунок
ARG user=django-user

# створюємо нового користувача (краще, ніж запускати все від root)
RUN adduser $user --disabled-password

# створюємо папку для проєкту і даємо користувачу права на неї
# щоб користувач мав право на роботу з цією папкою
# та всіма вкладеними папками
RUN mkdir -p /app && \
    chown -R $user /app

# копіюємо файл із залежностями
ADD ./requirements.txt ./requirements.txt

# переходимо на створеного користувача
USER $user

# додаємо папку з локально встановленими Python пакетами в PATH
# для простого запуску через 'python manage.py ...'
ENV PATH="$PATH/home/$user/.local/bin"

# оновлюємо pip і встановлюємо всі залежності проєкту
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# копіюємо весь код застосунку в контейнер
COPY . /app

# відкриваємо порт 8000 (на ньому працюватиме Django)
EXPOSE 8000

# команда, яка запускається при старті контейнера та
# запускає Django development сервер
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]