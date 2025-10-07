### Створення нового проекту або налаштування існуючого

1. Створення нового проекту з нуля:

```sh
poetry new django-project-demo
```

Після цього структура директорій буде такою:
```
.
├── django-project-demo
│   ├── pyproject.toml
│   ├── README.md
│   ├── src
│   │   └── django_project_demo
│   │       └── __init__.py
│   └── tests
│       └── __init__.py
```

Тут файл `pyproject.toml` тут є найважливішим. Він координуватиме ваш проект та його залежності.

2. Використання poetry для вже існуючого проекту:

```sh
cd my_django_proj
poetry init
```

Після цього структура вашого проекту не сильно зміниться, але додасться лише файл `pyproject.toml`:
```sh
.
├── accounts
├── core
├── db.sqlite3
├── manage.py
└── pyproject.toml
```

###  Режими роботи
`Poetry` може працювати у двох різних режимах. Режим за замовчуванням – це режим пакетування (бібліотеки), який є правильним, якщо ви хочете упакувати свій проект у `sdist` або `wheel` та, можливо, опублікувати його в індексі пакетів. У цьому режимі деякі метадані, такі як `name` та `version`, які потрібні для пакування (бібліотеки), є обов'язковими. Крім того, сам проект буде встановлено в режимі редагування під час запуску 'poetry install'.

Якщо ви хочете використовувати `Poetry` лише для керування залежностями, але не для пакування (бібліотеки), ви можете використовувати режим без пакетування. Для цього треба додати в `pyproject.toml` файл наступне:

```toml
[tool.poetry]
package-mode = false
```
У цьому режимі метадані, такі як name та version, є необов'язковими. Тому неможливо зібрати дистрибутив або опублікувати проект в індексі пакетів. Крім того, під час запуску `poetry install`, `Poetry` не намагається встановити сам проект, а лише його залежності, те що робить команда `poetry install --no-root`.

### Встановлення та налаштування інтерпретатора
Для того, щоб створити інтерпретатор в папці з проектом (як це робиться через `python -m venv .venv`), але використовуючи `poetry` треба зробити декілька налаштувань через термінал:
- `poetry config --list` - показує список всіх поточних налаштувань `poetry`
- `poetry config virtualenvs.in-project true` - активує створення папки із інтерпретатором в самому проекті (без цього налаштування інтерпретатор буде встановлено окремо в файловій системі в залежності від операційної системи)

Далі необхідно створити і встановити всі залежності, які прописані в файлі `pyproject.toml` командою:
```sh
poetry install --no-root
```

Як видно також поряд із файлом `pyproject.toml` з'явився файл `poetry.lock`. Цей файл містить в собі інформацію про встановлені всі залежності в проекті з їх точними версіями. Цей файл повинен бути обов'язково включений в GitHub репозиторій, щоб всі розробники завжди мали однакові версії залежностей для проекту.

Також в папці з проектом можна помітити папку `.venv`, яка автоматично створилась при виконанні попередньої команди.

Щоб подивитись всі встановлені залежності, треба не забути перейти в папку, яка містить наш `pyproject.toml` і виконати наступну команду:

```sh
poetry show
```

Ось її результат виконання (тут трошки більше пакетів, але приклад схожий):
```sh
asgiref   3.9.2  ASGI specs, helper code, and adapters
django    5.2.7  A high-level Python web framework that encourages rapid development and clean, pragmatic design.
iniconfig 2.1.0  brain-dead simple config-ini parsing
packaging 25.0   Core utilities for Python packages
pluggy    1.6.0  plugin and hook calling mechanisms for python
pygments  2.19.2 Pygments is a syntax highlighting package written in Python.
pytest    8.4.2  pytest: simple powerful testing with Python
sqlparse  0.5.3  A non-validating SQL parser.
```

Далі для виконання команд треба завжди використовувати команду `poetry run` (в папці з файлом `pyproject.toml`) перед вашою основною командою, наприклад:
```sh
poetry run python manage.py runserver
poetry run python manage.py makemigrations
poetry run python manage.py migrate
# і так далі
```
### Встановлення залежностей
Для того, щоб додати якусь залежність (бібліотеку) в ваш проект, можна це зробити декількома способами:
1. Через команду `poetry add <package>`, де `<package>` назва вашої бібліотеки.
    ```sh
    poetry add requests

    Updating dependencies
    Resolving dependencies... (0.4s)

    Package operations: 5 installs, 0 updates, 0 removals

    - Installing certifi (2025.8.3)
    - Installing charset-normalizer (3.4.3)
    - Installing idna (3.10)
    - Installing urllib3 (2.5.0)
    - Installing requests (2.32.5)
    ```
2. Через пряме додавання назви бібліотеки і версії в файл `pyproject.toml`.

    Наприклад, додамо бібліотеку `bcrypt` з версію 4.2.0 і вище.

    В файл `pyproject.toml` треба додати наступний запис в список `dependencies` - `"bcrypt >=4.2.0"`.

    І після цього запустити команду `poetry install --no-root` і ваша бібліотека буде встановлена.

Далі можна командою `poetry show` перевірити, що бібліотека була встановлена.

### Видалення залежностей

Для видалення залежностей також можна скористатись двома способами:
1. За допомогою команди `poetry remove <package>`, де `<package>` - назва залежності.
    ```sh
    poetry remove pytest

    Updating dependencies
    Resolving dependencies... (0.1s)

    Package operations: 0 installs, 0 updates, 5 removals

    - Removing iniconfig (2.1.0)
    - Removing packaging (25.0)
    - Removing pluggy (1.6.0)
    - Removing pygments (2.19.2)
    - Removing pytest (8.4.2)

    Writing lock file
    ```
2. Просто видаленням строки з назвою бібліотеки із файлу `pyproject.toml` із списку `dependencies` і запуском команди `poetry sync`.

Після цього файли `pyproject.toml` та `poetry.lock` будуть мати лише необхідні залежності.

Зверніть увагу, що після виконання команди `poetry sync` або `poetry install` може з'явитись наступне повідомлення:
```sh
Error: The current project could not be installed: Readme path `/home/sergey/Development/GoITeens/Django/poetry/my_django_proj/README.md` does not exist.
If you do not want to install the current project use --no-root.
If you want to use Poetry only for dependency management but not for packaging, you can disable package mode by setting package-mode = false in your pyproject.toml file.
If you did intend to install the current project, you may need to set `packages` in your pyproject.toml file.
```
Тут немає нічого страшного, тому як ви в основному будете використовувати `poetry` просто для керування залежностями, а не для пакетування вашого додатку (на сайт https://pypi.org), тому таке повідомлення просто вам про це говорить. Щоб цього повідомлення уникнути треба запускати команду із опцією `--no-root`:
- `poetry install --no-root`
- `poetry sync --no-root`