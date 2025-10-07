### Створення нового проекту або налаштування існуючого

Для створення нового проекту треба виконати наступну команду:
```sh
uv init uv-project-demo
cd uv-project-demo
```

Або можна вже ініціалізувати проект в існуючій директорії:
```sh
cd uv-project-demo
uv init
```

І далі можна побачити наступну структуру папок і файлів в папці `uv-project-demo`:
```sh
.
├── main.py
├── pyproject.toml
├── .python-version
└── README.md
```
Як видно, тут також присутній файл `pyproject.toml`, але поки із пустим списком залежностей.

### Встановлення залежностей
Для встановлення залежностей також як і в `Poetry` можна скористатись двома способами:
1. Запуск команди `uv add <package>`, де `<package>` - назва бібліотеки (залежності) для встановлення.
    ```sh
    uv add django

    Using CPython 3.13.7 interpreter at: /usr/bin/python3
    Creating virtual environment at: .venv
    Resolved 5 packages in 620ms
    Prepared 2 packages in 1.47s
    Installed 3 packages in 152ms
    + asgiref==3.9.2
    + django==5.2.7
    + sqlparse==0.5.3W
    ```

    І тепер після цього в файлі `pyproject.toml` буде присутня наша залежність:
    ```toml
    dependencies = [
    "django>=5.2.7",
    ]
    ```
    Як видно після цього з'явився файл `uv.lock` із точними версіями залежностей для вашого проекту. Цей файл має такий же самий формат як і `poetry.lock` і цей файл також повинен бути включений в GitHub репозиторій, щоб кожен розробник мав однакові версії бібліотек для проекту.

2. Додати назву залежності із потрібною версією напряму в файл `pyproject.toml` і після цього запустити команду `uv sync`. Додамо строку `"bcrypt >=4.2.0"` в `dependencies`.
```sh
uv sync

Resolved 6 packages in 7ms
Installed 1 package in 9ms
 + bcrypt==5.0.0
```

Для того, щоб перевірити, які залежності вже встановлені, треба запустити команду:
```sh
uv tree

Resolved 6 packages in 0.79ms
uv-project-demo v0.1.0
├── bcrypt v5.0.0
└── django v5.2.7
    ├── asgiref v3.9.2
    └── sqlparse v0.5.3
```

### Видалення залежностей
Для того, щоб видалити залежності, теж можна (як і в `poetry`) скористатись двома методами:
1. Запустивши команду `uv remove <package>`, де `<package>` - назва бібліотеки (залежності) для встановлення.

    ```sh
    uv remove bcrypt

    Resolved 5 packages in 334ms
    Uninstalled 1 package in 0.44ms
    - bcrypt==5.0.0
    ```
2. Просто видаливши строку із назвою залежності (бібліотеки) із файлу `pyproject.toml` і запустити команду `uv sync`.
    Видалимо `django` і запустимо команду `uv sync`. Після цього запустимо команду `uv tree`:
    ```sh
    Resolved 1 package in 3ms
    Uninstalled 3 packages in 165ms
    - asgiref==3.9.2
    - django==5.2.7
    - sqlparse==0.5.3

    uv tree
    Resolved 1 package in 0.82ms
    uv-project-demo v0.1.0
    ```

Як видно, більше немає ніяких встановлених бібліотек в проекті.

### Запуск команд

Так само як і в `poetry` треба робити запуск команд через команди `uv`:
```sh
uv run python manage.py runserver
uv run python manage.py makemigrations
uv run python manage.py migrate

# і так далі
```