# Домашнє завдання: Kubernetes (Minikube)

## Мета

Оновити поточний Kubernetes-проєкт так, щоб він став ближчим до production-підходу.

У завданні потрібно попрацювати з:

* `Secret`
* `ConfigMap`
* `Deployment`
* `Service`
* `readinessProbe` / `livenessProbe`

`ConfigMap` та `readinessProbe` / `livenessProbe` ще не розглядали, але вони налаштовуються не складно.

---

# 1. Розділення Secret і ConfigMap

У поточному backend використовується один `Secret`, у якому знаходяться і секретні, і звичайні конфігураційні змінні.

## Потрібно:

* створити окремий `ConfigMap`
* винести туди звичайні конфігураційні значення
* залишити в `Secret` лише секретні дані
* підключити `Secret` і `ConfigMap` до backend `Deployment`

## Підказка

Подумайте, які змінні:

* можна зберігати відкрито
* не повинні зберігатися відкрито

### До ConfigMap логічно винести:

* `DEBUG`
* `ALLOWED_HOSTS`
* `POSTGRES_HOST`
* `POSTGRES_PORT`

### У Secret залишити:

* `POSTGRES_PASSWORD`
* `SECRET_KEY`

## Secret потрібно записати через `data`

Не через:

```yaml
stringData:
```

а через:

```yaml
data:
```
і дані в `data` повинні бути в `base64` кодуванні!


## Як отримати base64

### Windows PowerShell

```powershell
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("your_value"))
```

### Онлайн-ресурс

Можна використати будь-який Base64 encoder ([Наприклад](https://www.base64encode.org/))

---

# 2. Додати `readinessProbe` та `livenessProbe`

У backend `Deployment` потрібно додати перевірку стану контейнера.

## Потрібно:

створити окремі endpoint-и у Django:

* `/health/live/`
* `/health/ready/`

## Що має робити endpoint

Повернути просту відповідь:

* HTTP 200
* короткий `JSON` або текст

Наприклад:

```json
{"status": "ok"}
```

## Приблизна ідея probes

```yaml
readinessProbe:
  httpGet:
    path: /health/ready/
    port: 8001

livenessProbe:
  httpGet:
    path: /health/live/
    port: 8001
```

## Перевірити результат

```bash
minikube kubectl -- describe pod <pod-name>
```

* `readinessProbe` — коли pod готовий приймати трафік
* `livenessProbe` — коли pod потрібно перезапустити

---

# 3. Додати ще один сервіс у cluster

Створити окремий сервіс, який працює в Kubernetes.

## Потрібно:

* створити `Deployment`
* створити `Service`

## Варіанти

* новий web-інтерфейс
* сервіс для роботи з БД (можна Adminer, як я показував на уроці про Docker Compose)
* будь-який lightweight container

Можете загуглити, що це може бути :)

## Подумайте

чи потрібен:

* `NodePort`
* або достатньо `ClusterIP`

---

# 4. Перевірка результату

```bash
minikube kubectl -- get pods
minikube kubectl -- get svc
minikube kubectl -- get configmap
minikube kubectl -- get secret
minikube kubectl -- get deploy
```

## Коротко пояснити

* що винесли в `ConfigMap`
* що залишили в `Secret`
* чому обрали саме такий тип `Service`
---

# Важливо

Не забувайте про послідовність примінення маніфестів - спочатку те, від чого залежить `Deployment`, а потім вже сам `Deployment`.
Щоб отримати доступ до вашого додатку з локального комп'ютера треба застосувати команду `minikube service <service_name>`--url і далі вже за отриманим посиланням можна переходити в браузер. Зверніть увагу, що таке можливо лише з типом сервісу `NodePort`, яким в нашому випадку є Django сервіс.
