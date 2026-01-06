# Git — гілки, merge, reset та config

## Початкові умови

1. Створіть **новий репозиторій** на GitHub
2. Клонуте його локально
3. Основна гілка — `main`

## 1. Git config (обовʼязково)

Перед початком роботи перевірте Git-конфігурацію:

```bash
git config --list
```

Переконайтесь, що задані:
- `user.name`
- `user.email`

Якщо ні — налаштуйте:

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

Всі комміти **повинні мати коректного автора**

## Структура проекту

У корені репозиторію створіть файл:

```
project.txt
```

### Початковий вміст `project.txt`

```
Project: Git Practice
Version: 1.0

Features:
- Base structure
```

Зробіть **перший комміт** у гілці `main` з комміт повідомленням:

```
Initial project structure
```

## 2. Гілка `feature-login`

1. Створіть гілку:
   ```
   feature-login
   ```

2. У файлі `project.txt` додайте у розділ `Features`:
   ```
   - Login system
   ```

3. Зробіть комміт:
   ```
   Add login feature
   ```

4. Додайте ще один пункт:
   ```
   - Remember me option
   ```

5. Зробіть **другий комміт**:
   ```
   Extend login feature
   ```

## 3. Merge у `main`

6. Перейдіть у гілку `main`
7. Обʼєднайте `feature-login` у `main` **через merge**
8. Перевірте історію коммітів:
   ```bash
   git log
   # або
   git log --oneline --graph
   ```

## 4. Гілка з помилкою `feature-payment`

9. Створіть гілку:
   ```
   feature-payment
   ```

10. У файлі `project.txt`:
    - змініть версію:
      ```
      Version: 2.0
      ```
    - додайте у `Features`:
      ```
      - Payment system
      ```

11. Зробіть комміт:
    ```
    Add payment feature
    ```

12. Цей пункт додасть `помилка` (звісно не реальну):  
    Видаліть рядок:
    ```
    Project: Git Practice
    ```

13. Зробіть ще один комміт:
    ```
    Update payment logic
    ```

---

## 5. Відкат змін (reset)

14. Подивіться історію коммітів:
    ```bash
    git log
    ```

15. Знайдіть комміт **до помилки**

16. Послідовно виконайте:
    ```bash
    git reset --soft <hash>
    git status
    ```

    ```bash
    git reset --mixed <hash>
    git status
    ```

    *(опціонально)*  
    ```bash
    git reset --hard <hash>
    ```

При **`--hard` НЕ пушити**


## 6. Відновлення через reflog

17. Перегляньте історію дій:
    ```bash
    git reflog
    ```

18. Відновіть стан репозиторію **до reset**

19. Переконайтесь, що файл `project.txt` знову містить всі зміни

## 7. Завершення

20. Видаліть гілку:
    ```
    feature-payment
    ```

21. Запуште фінальний стан гілки `main` у GitHub

## Результат

У репозиторії має бути:
- мінімум **2 гілки**
- **merge**
- **reset**
- **reflog**
- коректний **author** у всіх коммітах

## Що здати

1. Скрін або текст команди:
   ```bash
   git log --oneline --graph
   ```

2. Коротко (2–3 речення):
   - де була помилка
   - як ви її відкотили
   - що відбувалось з файлами після `reset`

## Заборонено (не рекомендується)

- Робити `rebase`
- Пушити `reset --hard`
- Видаляти історію коммітів на GitHub
