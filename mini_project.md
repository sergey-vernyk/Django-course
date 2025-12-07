# Створити невеликий міні-блог із такими можливостями

Створити проект `blog_project`

### Applications:
- `accounts`
- `articles`

### Requirements:
- реєстрації користувача (`accounts`);
- входу/виходу з системи (`accounts`);
- створення статей (тільки для авторизованих) (`articles`);
- перегляду списку статей з пагінацією (`articles`);
- перегляду окремої статті (`articles`);
- використання шаблонів, `include`, тегів і фільтрів (`articles`).

### Models:
`Article`:
- `title`: `CharField`, `max_length=200`.
- `content`: `TextField`.
- `created_at`: `DateTimeField`, `auto_now_add=True`.
- `author`: `ForeignKey`, `User`, `on_delete` -> `CASCADE`.

`User`:
Вбудований ->`from django.contrib.auth.models import User`.
Просто імпортувати, створювати не потрібно!

### Forms:
- `ArticleForm` -> `ModelForm` (Модель `Article`). 
    Поля:
    - `title`,
    - `content`.
- `RegisterForm` -> `ModelForm` (Модель `User`).
    Поля:
    - `username`,
    - `email`,
    - `password`. 
    
    Віджет на поле `password` -> `forms.PasswordInput`

### Views:
`articles:`
- `article_list` -> додати пагінатор на 5 статей на одну сторінку.
- `article_create` -> додати поточного авторизованого користувача як автора посту. Редірект на список з постами після створення.
- `article_detail` -> детальна інформація про статтю

`accounts`:
- `register` -> зберігати пароль в захешованому виді в БД, викликати `login(request, user)` після успішного створення користувача. При помилках - відображати форму з помилками.

- `UserLoginView(LoginView)` -> `from django.contrib.auth.views import LoginView`. Віднаслідувати від `LoginView` і перевизначити `template_name` на ваш кастомний шаблон для логіну.
- `LogoutView` -> `from django.contrib.auth.views import LogoutView`

### URLS:
`articles`:
- `''` -> Список статей,
- `<int:pk>/` -> Детальна інформація про статтю
- `create/` -> Створити статтю

`accounts`:
- `register/` -> Реєстрація
- `login/` -> Логін
- `logout/` -> Вихід

`blog_project`(global `urls.py`):
- `articles/` -> `include('articles.urls')`
- `accounts/`-> `include('accounts.urls')`


### Templates:
#### Теги:
- `{% extends %}`
- `{% include %}`
- `{% url %}`
- `{% csrf_token %}`
- `{% for %}`
- `{% empty %}`
- `{% if %}`
- `{% block %}`
- `{% load static %}`

#### Фільтри:
- `date`
- `truncatewords`
- `length`
- `upper або lower`
- `default`
- `pluralize`
- `linebreaks`

#### Шаблони
- `articles -> templates` (розширюють `base.html`):
    - `list.html`
    - `detail.html`
    - `create.html`

- `accounts -> templates -> accounts` (розширюють `base.html`):
    - `login.html`
    - `register.html`

- `blog_project -> templates`:
    - `base.html`
    - `paginator.html`
    - `components -> article_card.html`
    - `layout -> navigation.html`
    - `layout -> footer.html`



### Приблизна структура:
```sh
blog_project/
├── blog_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── articles/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/
│       └── articles/
│           ├── list.html
│           ├── detail.html
│           └── create.html
│
├── accounts/
│   ├── __init__.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/
│       └── accounts/
│           ├── login.html
│           └── register.html
│
├── templates/
│   ├── base.html
│   ├── paginator.html
│   ├── components/
│   │   └── article_card.html
│   └── layout/
│       ├── navigation.html
│       └── footer.html
│
└── manage.py

```