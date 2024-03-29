# Учебный проект  API YaMDb

## Описание:

Проект YaMDb собирает **отзывы** пользователей на **произведения**. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на **категории**, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Произведению может быть присвоен **жанр** из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).

Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые **отзывы** и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — **рейтинг** (целое число). На одно произведение пользователь может оставить только один отзыв.

Пользователи могут оставлять **комментарии** к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

## Как запустить проект

1. Клонировать репозиторий

git clone https://github.com/alexey-boborykin/infra_sp2.git

2. Создать файл .env по шаблону

DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
SECRET_KEY="string"

3. Из директории infra_sp2/infra/ sвполнить команду 

docker-compose up -d

4. Выполнить миграции 

docker-compose exec web python manage.py migrate

5. Создать суперпользователя

docker-compose exec web python manage.py createsuperuser

6. Собрать статику

docker-compose exec web python manage.py collectstatic --no-input

7. При необходимости заполнить базу тестовыми данными

docker-compose exec web python manage.py loaddata fixtures.json

## Ресурсы API **YaMDb**

-   Ресурс **auth:** аутентификация.
-   Ресурс **users:** пользователи.
-   Ресурс **titles:** произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
-   Ресурс **categories:** категории (типы) произведений («Фильмы», «Книги», «Музыка»). Одно произведение может быть привязано только к одной категории.
-   Ресурс **genres**: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
-   Ресурс **reviews:** отзывы на произведения. Отзыв привязан к определённому произведению.
-   Ресурс **comments:** комментарии к отзывам. Комментарий привязан к определённому отзыву.

## Примеры запросов и получаемых ответов:

1. Самостоятельная регистрация пользователя.

### Запрос:

```
POST http://127.0.0.1:8000/api/v1/auth/signup/
Content-Type: application/json

{
    "email": "user@example.com",
    "username": "string"
}
```
### Ответ:
```
{
    "email": "string",
    "username": "string"
}
```

2. Получение JWT-токена (необходимо передать полученный код подтверждения).

### Запрос:
```
POST http://127.0.0.1:8000/api/v1/auth/token/
Content-Type: application/json

{
    "username": "string",
    "confirmation_code": "string"
}
```

### Ответ:
```
{
    "token": "string"
}
```

Более подробная информация о возможных запросах и получаемых ответах находится в документации.

## Документация
После запуска проекта документация будет доступна по адресу: 
http://127.0.0.1:8000/redoc
