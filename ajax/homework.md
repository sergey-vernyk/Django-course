# Динамічні коментарі та лайки через AJAX + jQuery

## Структура проекту (приклад)

```
myproject/
├── manage.py
├── myapp/
│   ├── models.py         # моделі Post та Comment
│   ├── views.py          # додавання/видалення коментарів, лайки/дизлайки
│   ├── urls.py
│   └── templates/
│       └── myapp/
│           └── posts.html   # HTML зі списком постів та коментарями
├── static/
│   └── js/
│       └── comments.js   # файл для основної логіки AJAX запитів
└── ...
```
## Моделі

- **Post**
  - title (CharField)
  - content (TextField)
  - likes (IntegerField, default=0)
  - dislikes (IntegerField, default=0)

- **Comment**
  - post (ForeignKey -> Post)
  - text (TextField)
  - created_at (DateTimeField)

## Views

- `add_comment(request: HttpRequest) -> JsonResponse`
  - `POST`
  - отримує `post_id` та текст коментаря
  - додає коментар у базу
  - повертає `JSON` з текстом, id та новим лічильником коментарів

- `delete_comment(request: HttpRequest, comment_id: int) -> JsonResponse`
  - `POST`
  - видаляє коментар
  - повертає `JSON` з оновленим лічильником коментарів

- `like_post(request: HttpRequest, post_id: int) -> JsonResponse`
  - `POST`
  - збільшує `likes` на 1
  - повертає `JSON` з оновленим рахунком

- `dislike_post(request: HttpRequest, post_id: int) -> JsonResponse`
  - `POST`
  - збільшує dislikes на `1`
  - повертає `JSON` з оновленим рахунком

## HTML-шаблон (`posts.html`), але можете і свій зробити

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Posts</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
</head>
<body>

<form method="post" style="display: none;">
    {% csrf_token %}
</form>

<div class="container mt-4">
    <h1>Posts</h1>
    {% for post in posts %}
        <div class="card mb-4">
            <div class="card-body">
                <h5 class="card-title">{{ post.title }}</h5>
                <p class="card-text">{{ post.content }}</p>

                <!-- лайк / дізлайк -->
                <div>
                    <button class="btn btn-sm btn-success like-button" data-id="{{ post.id }}">Like</button>
                    <button class="btn btn-sm btn-danger dislike-button" data-id="{{ post.id }}">Dislike</button>
                    <span>Likes: <span id="likes-count-{{ post.id }}">{{ post.likes }}</span></span>
                    <span>Dislikes: <span id="dislikes-count-{{ post.id }}">{{ post.dislikes }}</span></span>
                </div>

                <!-- коментарі -->
                <div class="mt-3">
                    <h6>Comments (<span id="comments-count-{{ post.id }}">{{ post.comment_set.count }}</span>)</h6>
                    <ul id="comments-list-{{ post.id }}" class="list-group mb-2">
                        {% for comment in post.comment_set.all %}
                            <li class="list-group-item" id="comment-{{ comment.id }}">
                                {{ comment.text }}
                                <button class="btn btn-sm btn-outline-danger delete-comment" data-id="{{ comment.id }}">Delete</button>
                            </li>
                        {% empty %}
                            <li class="list-group-item">No comments yet.</li>
                        {% endfor %}
                    </ul>

                    <!-- додати коментар -->
                    <div class="input-group mb-3">
                        <input type="text" class="form-control comment-input" placeholder="Add a comment..." data-post-id="{{ post.id }}">
                        <button class="btn btn-primary add-comment" data-post-id="{{ post.id }}">Add</button>
                    </div>
                </div>
            </div>
        </div>
    {% endfor %}
</div>

<script src="{% static 'js/comments.js' %}" type="module"></script>
</body>
</html>
```

## Підказки по jQuery

### Отримати CSRF токен (так як і на уроці було)

```js
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export default getCookie
```

### AJAX POST для додавання коментаря

- Використати `$.ajax({ url, method, data, success })`  
- У `success` додати новий `<li>` у DOM:  
```js
$("#comments-list-" + postId).append(`<li id="comment-${response.id}">${response.text}</li>`);
```

### Видалення коментаря

- В click handler використати:  
```js
$(`#comment-${commentId}`).remove();
```
- Оновити лічильник коментарів

### Лайки / Дизлайки

- В click handler для кнопок Like/Dislike:  
```js
$("#likes-count-" + postId).text(response.likes);
$("#dislikes-count-" + postId).text(response.dislikes);
```

- Використати `data-id` на кнопках для визначення посту

## Поради

- Bootstrap для стилізації карток, кнопок та списку коментарів  
- JSON відповіді від сервера повинні містити актуальні дані: текст, id, лічильники  
- Ви пишете **свій JS** у `static/js/comments.js`, використовуючи підказки (ну або якщо знаєте як краще - то без підказок)
- [jQuery Documentation](https://api.jquery.com) - ось сайт з документацією по jQuery, якщо треба знайти (або просто цікаво), як будь-який метод працює.
