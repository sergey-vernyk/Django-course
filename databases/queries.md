## Запити до БД на сайті https://www.pgtutorial.com/playground/

```sql
-- Агрегатна функція SUM
SELECT 
  warehouse_id, 
  SUM(quantity) as amount_quantity_per_warehouse 
FROM 
  inventories 
GROUP BY 
  warehouse_id;
```
```sql
-- Агрегатна функція COUNT
SELECT 
  warehouse_id, 
  COUNT(inventory_id) as amount_inventory 
FROM 
  inventories 
GROUP BY 
  warehouse_id;
```

```sql
-- Фільтр WHERE з null
SELECT 
  profiles.first_name, 
  profiles.last_name, 
  users.email, 
  profiles.work_phone 
FROM 
  profiles 
  INNER JOIN users ON users.user_id = profiles.user_id 
WHERE 
  profiles.work_phone is NULL;
```

```sql
-- Агрегатні функції MAX, MIN, AVG та групування з GROUP BY
SELECT 
  brands.brand_name, 
  MAX(price) as max_price, 
  MIN(price) as min_price, 
  ROUND(
    AVG(price), 
    2
  ) as avarage_price 
FROM 
  brands 
  INNER JOIN products ON brands.brand_id = products.brand_id 
GROUP BY 
  brands.brand_name;
```

```sql
-- Використання фільтра HAVING
SELECT 
  brands.brand_name, 
  MAX(price) as max_price, 
  MIN(price) as min_price, 
  ROUND(
    AVG(price), 
    2
  ) as avarage_price 
FROM 
  brands 
  INNER JOIN products ON brands.brand_id = products.brand_id
  -- WHERE MAX(price) > 2000.0 - так не можна!
GROUP BY 
  brands.brand_name 
  HAVING MAX(price) > 2000.0;
```
```sql
-- Створення таблиці із значенням за замовчуванням
CREATE TABLE invoices (
created timestamp default current_timestamp, 
value VARCHAR(30), 
id serial primary key
);
```

```sql
-- вставка даних в таблицю лише значення 'value', а не 'created'
INSERT INTO invoices (value) 
VALUES 
  ('zxcvb');
INSERT INTO invoices (value) 
VALUES 
  ('zxcvb456');
``` 
```sql
-- Регулярні вирази з LIKE, ILIKE (регістро-незалежний пошук)
SELECT 
  * 
FROM 
  products 
WHERE 
  product_name ILIKE '%max%';
```
```sql
-- Пустий результат, так як 'max' не існує в БД, а тільки 'Max'
SELECT 
  * 
FROM 
  products 
WHERE 
  product_name LIKE '%max%';
```
```sql
-- Створення кастомного типу (стать)
CREATE TYPE gender_type as ENUM ('F', 'M');
```
```sql
-- Отримання інформації по новоствореному типу (просто перевірка, що він створився)
SELECT 
  * 
FROM 
  pg_catalog.pg_type 
WHERE 
  pg_type.typname = 'gender_type';
```

```sql 
-- Додавання нової колонки в таблицю 'profiles' із новоствореним типом вище
ALTER table 
  profiles 
ADD 
  column gender gender_type;
```

```sql  
-- Оновлення існуючих записів в таблиці profiles
-- встановлення статі для записів користувача
UPDATE 
  profiles 
SET 
  gender = 'M' 
WHERE 
  user_id IN (1, 3, 5);

UPDATE 
  profiles 
SET 
  gender = 'F' 
WHERE 
  user_id IN (2, 4);
```

```sql
-- перевірка, що поле gender було оновлено
SELECT 
  * 
FROM 
  profiles 
WHERE 
  gender = 'F';
```  

```sql
-- додавання поля 'user_id' до вище створеної таблиці
ALTER TABLE 
  invoices 
ADD 
  COLUMN user_id INTEGER;

-- конфігурація цього поля як ForeignKey на таблицю 'users'
ALTER TABLE 
  invoices 
ADD 
  CONSTRAINT fk_users FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE;

-- оновлення існуючих записів в invoices (рандомне призначення user на таблицю 'invoices')
UPDATE 
  invoices 
SET 
  user_id = 5 
WHERE 
  id = 1;

UPDATE 
  invoices 
SET 
  user_id = 3 
WHERE 
  id = 2;
```
```sql
-- Об'єднання таблиць 'users' та 'invoices'
SELECT 
  * 
FROM 
  invoices 
  INNER JOIN users ON invoices.user_id = users.user_id;
```
```sql
-- Створення функції
CREATE 
OR REPLACE FUNCTION get_quantity_per_warhouse () RETURNS TABLE (
  warehouse_id integer, amount_quantity_per_warehouse integer
) AS $$ 
SELECT 
  warehouse_id, 
  SUM(quantity) as amount_quantity_per_warehouse 
FROM 
  inventories 
GROUP BY 
  warehouse_id;
$$ LANGUAGE SQL;
```
```sql
-- Виклик створеної функції (дужки обов'язкові)
SELECT 
  * 
FROM 
  get_quantity_per_warehouse();
```
```sql  
-- Створення view
CREATE VIEW products_in_warehouse AS 
SELECT 
  w.warehouse_name, 
  u.user_id, 
  CONCAT(pr.first_name, ' ', pr.last_name) AS user_name, 
  SUM(quantity) AS products_per_user 
FROM 
  warehouses w 
  INNER JOIN transactions t ON t.warehouse_id = w.warehouse_id 
  INNER JOIN users u ON u.user_id = t.user_id 
  INNER JOIN profiles pr ON pr.user_id = u.user_id 
GROUP BY 
  w.warehouse_name, 
  user_name, 
  u.user_id 
ORDER BY 
  products_per_user;
```
```sql
-- Виклик view (як звичайного запиту)
SELECT 
  * 
FROM 
  products_in_warehouse;
```