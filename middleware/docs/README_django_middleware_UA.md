# Django Middleware — Конспект та практика

## Що таке Middleware:

Middleware у Django — це шар між HTTP-запитом і view.

Він може:
- змінювати `request`
- зупиняти виконання
- змінювати `response`
- обробляти помилки

## Як рухається запит:

```
Request ->
   Middleware A (request)
   Middleware B (request)
       -> VIEW ->
   Middleware B (response)
   Middleware A (response)
<- Response
```

- Запит іде **зверху вниз**
- Відповідь повертається **знизу вверх**

---

## Вбудовані Middleware (основні)

### 🔐 SecurityMiddleware
- додає security headers
- може примусово включати HTTPS

### 🍪 SessionMiddleware
- додає `request.session`
- зберігає дані між запитами

### 👤 AuthenticationMiddleware
- додає `request.user`
- визначає, хто авторизований

### 🛡 CsrfViewMiddleware
- захищає від CSRF атак
- перевіряє:
  - CSRF token
  - заголовки Referer / Origin

### 🧰 CommonMiddleware
- редіректи (`/page` -> `/page/`)
- дрібні HTTP-покращення

### 💬 MessageMiddleware
- одноразові повідомлення (flash messages)
- використовує `session` або `cookies`

### 🛡 XFrameOptionsMiddleware
- захист від clickjacking
- додає header відповіді: `X-Frame-Options: DENY`

---

## Middleware Hooks

### `__init__(get_response)`
- викликається 1 раз при старті
- використовується для ініціалізації

### `__call__(request)`
- викликається на кожен запит
- обгортає весь lifecycle

```python
def __call__(self, request: HttpRequest) -> HttpResponse:
    # ДО view
    response = self.get_response(request)
    # ПІСЛЯ view
    return response
```

### `process_view()`
- викликається перед view
- може:
  - перевіряти доступ
  - зупиняти виконання

### `process_exception()`
- викликається, якщо view впав
- може повернути власний response

### `process_template_response()`
- викликається, якщо response має `.render()`
- (наприклад TemplateResponse)
- дозволяє змінити HTML перед відправкою

### `process_response()`
- викликається для КОЖНОГО response
- навіть якщо була помилка
- використовується для:
  - додавання headers
  - логування

---

## Повний життєвий цикл

```
1. __init__()                  -> 1 раз
2. __call__()                  -> перед get_response()
3. process_view()
4. view()
5. process_exception()         -> якщо помилка (Exception)
6. process_template_response() -> якщо HTML response (TemplateResponse)
7. __call__()                  -> після get_response()
```
---

## Практичні експерименти

### ❌ Прибрати `CsrfViewMiddleware`
- ✔ все працює
- ❌ немає захисту

### ❌ Прибрати `SessionMiddleware`
- ❌ не працює `login`
- ❌ немає `session`
- ❌ не працюють `messages`

### ❌ Прибрати `AuthenticationMiddleware`
- ❌ `request.user` відсутній
- ❌ `@login_required` не працює
- ❌ `admin` ламається

---

## Чому щось ламається?

Django може працювати без деяких middleware, але:

> Інші компоненти ОЧІКУЮТЬ їх наявність

Наприклад:
- `admin` використовує session + auth + messages

## Clickjacking (базове пояснення)

`Clickjacking` — це атака, коли:

- користувач думає, що клікає кнопку
- але насправді клікає елемент у невидимому `iframe`

### Як це працює

- iframe накладається поверх UI
- робиться майже прозорим
- користувач не бачить реальну дію

Захист - додавання заголовку `X-Frame-Options: DENY` 

Блокує відкриття сторінки в `iframe`.

## Коли використовувати Middleware?

| Ситуація | Рішення |
|---------|--------|
| Логіка для всіх запитів | Middleware |
| Логіка для одного view | Decorator |

---

## Фінальний висновок

> Middleware — це фундамент Django

Без нього:
- немає авторизації
- немає безпеки
- немає нормальної обробки запитів
