# Цель проекта
Данный проект представляет собой систему хранения информации о произведениях искусства.
Сама система не предусматривает хранение, непосредственно, этих произведений, а только описания/отзывы.

## Загрузка данных
Загрузка данных может произведена с помощью команды:  
*python manage.py upload_csv {table_name} [--filename {filename}]*

Поле "filename" опциональное.  
Если оно не указано, система попробует получить файл по пути:  
\static\data\\{table_name.csv}

Категория произведения (Category) является **обязательной** для произведения (Title), следовательно, **загрузку категорий нужно выполнять до загрузки произведений**.  
Аналогично для загрузки привязок "Произведние - Жанр", чтобы создать привязки, таблицы Произведение и Жанр должны уже существовать.  

## Команда для запуска проекта 
*docker-compose up*  
*docker-compose exec web python manage.py makemigrations --noinput*  
*docker-compose exec web python manage.py migrate --noinput*  
*docker-compose exec web python manage.py collectstatic --no-input*  

## Kоманда для создания суперпользователя
*docker-compose exec web python manage.py createsuperuser*  

## Команда для заполнения базы начальными данными
*docker-compose exec web python manage.py loaddata fixtures.json*  

## Для подключения к базе данных
требуется скопировать и отредактировать файл .env  
*cp .env.template .env*
