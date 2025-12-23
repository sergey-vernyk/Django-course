# Django Signals + Cache

---

## Опис проекту

Створити mini-project `Subscriptions`, де користувач може підписуватися на теми (`Topic`).

Система повинна:
- показувати список тем користувача
- відображати кількість підписників теми
- використовувати кеш для швидкого доступу
- використовувати вбудовані та кастомні сигнали для автоматичної інвалідації кешу та створення активностей

## Кроки

1. Створити новий Django-проєкт та app:

```sh
django-admin startproject core
cd core
python manage.py startapp topics
```

2. Додати app в `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    "topics",
]
```

3. Використовувати стандартну модель `User`.

## Моделі

#### Topic
- `name` -> `CharField` max_length=100, unique
- `subscribers` -> `ManyToManyField` на `User`, `related_name` - "topics", blank

#### TopicActivity
- `topic` -> `ForeignKey` на `Topic`, `on_delete`- models.CASCADE, `related_name` - "activities"
- `action` -> `CharField`, max_length - 20, `choices` -> "created","deleted", "updated"
- `created_at` -> `DateTimeField`,  `auto_now_add`-True

## Міграція даних (як робили на уроці)

Після `migrate` (можна в другій міграції робити) повинні існувати теми (`Topic` об'єкти):
- Python
- Django
- DevOps

Реалізувати через `RunPython`.

## URLs
 
В `topics` додатку:
- `""` -> GET (список тем користувача)
- `"subscribe/<id>/"` -> POST (підписатися)       
- `"unsubscribe/<id>/"` -> POST (відписатися)         
- `"create/"` -> POST (створити тему)    
- `"delete/<id>/"` -> POST (видалити тему)

В `core`(додати):
- `path("topics/", include("topics.urls"))`

## Views

### 1. `topics_view`

- доступ тільки для залогінених (треба відповідний декоратор)
- повертає HTML зі списком тем
- кешує список тем користувача за ключем: `user:{user_id}:topics` (ключ для отримання і встановлення в кеш з методами `get`, `set` або `delete`).
- TTL (час життя даних в кеші) = 60 секунд

### 2. `subscribe_view, unsubscribe_view`

- змінюють `m2m` поле `subscribers`
- не чистять кеш

### 3. `create_topic_view`

- створює `Topic` об'єкт
- не чистить кеш
- не створює `TopicActivity`

### 4. `delete_topic_view`

- видаляє `Topic`
- не чистить кеш
- не створює `TopicActivity`

(!) Вся логіка автоматичного створення activity та інвалідації (очищення) кешу реалізується через сигнали.

## Сигнали

### `topics/signals.py`

#### 1. `m2m_changed`

- для `Topic.subscribers.through`
- події: `post_add`, `post_remove`, `post_clear`
- інвалідує кеш користувача

#### 2. `post_save` для `Topic`

- при створенні (`created=True`) створює `TopicActivity(action="created")`

#### 3. `post_delete` для `Topic`

- створює `TopicActivity(action="deleted")`

## Кастомний сигнал ([Посилання на туторіал](https://medium.com/dajngo/custom-signals-in-django-2e9986925579))

### Створити кастомний сигнал в `topics/signals.py`

```python
from django.dispatch import Signal

topic_changed = Signal()
```

- Надсилати його з `post_save`, `post_delete` (саме з обробника сигналу на post_save / post_delete для Topic)
- Логіка обробника кастомного сигналу (receiver):
  - логування дій: `Topic {topic_id} changed: {action}`
  - інвалідація кешу користувача по його topic-ам.

Приклад надсилання:
```python
topic_changed.send(sender=sender, topic_id=instance.id, action=action)
```

## Підключення сигналів

Через `apps.py`:

```python
class TopicsConfig(AppConfig):
    name = "topics"

    def ready(self):
        from . import signals
        # важливо підключити не вбудований (кастомний) сигнал
        signals.topic_changed.connect(signals.handle_topic_changed)
```

## Шаблони

### `templates/topics/topics.html`

- Список всіх тем
- Показати кількість підписників
- Кнопки:
  - Subscribe / Unsubscribe
  - Delete
- Позначити, чи користувач підписаний

## Що повинно бути в результаті

- `Activity` створюється автоматично через сигнали
- Кеш інвалідується тільки(!) через сигнали
- Є `post_save`, `post_delete`, `m2m_changed`
- Використовується кастомний сигнал
- Views мінімальні, без бізнес-логіки

## Бонус (хто хоче)
- Використати сигнал `user_logged_out` для очистки кешу
