## Процес встановлення залежностей та запуску сервера

#### 1. Створити віртуальне оточення:
```sh
python -m venv .venv
```

#### 2. Активувати його:
```sh
# Linux/Mac
source .venv/bin/activate

# Windows Cmd
.venv\Scripts\activate.bat

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows Git Bash
source .venv/Scripts/activate
```

#### 3. Встановити залежності (якщо є файл):
```sh
pip install -r requirements.txt
```

#### 4. Запустити `django` server:
```sh
# перейти в директорію з файлом manage.py і запустити
python manage.py runserver 

```