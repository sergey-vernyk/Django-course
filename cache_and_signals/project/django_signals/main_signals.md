### Сигнали моделей (django.db.models.signals)

| Сигнал        | Коли викликається   |
| ------------- | --------------------|
| `pre_save`    | перед `save()`      |
| `post_save`   | після `save()`      |
| `pre_delete`  | перед `delete()`    |
| `post_delete` | після `delete()`    |
| `pre_init`    | після `__init__()`  |
| `post_init`   | після `__init__()`  |
| `m2m_changed` | зміни ManyToMany    |

### Сигнали request/response
| Сигнал             | Опис                |
| ------------------ | ------------------- |
| `request_started`  | початок HTTP-запиту |
| `request_finished` | кінець HTTP-запиту  |

### Сигнали migrate
| Сигнал             | Опис                        |
| -------------------| ----------------------------|
| `pre_migrate`      | початок примінення міграції |
| `post_migrate`     | кінець примінення міграції  |


