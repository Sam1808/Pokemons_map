# Карта покемонов

![sample text](https://dvmn.org/filer/canonical/1563275070/172/)

### Предметная область

Сайт для помощи по игре [Pokemon GO](https://www.pokemongo.com/en-us/). Это игра про ловлю [покемонов](https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D0%BA%D0%B5%D0%BC%D0%BE%D0%BD).

Суть игры в том, что на карте периодически появляются покемоны, на определённый промежуток времени. Каждый игрок может поймать себе покемона, и пополнить свою личную коллекцию.

На карте может быть сразу несколько особей одного и того же покемона: например, 3 Бульбазавра. Каждую особь могут поймать сразу несколько игроков. Если игрок поймал себе особь покемона, она исчезает для него, но остаётся для других.

В игре есть механика эволюции. Покемон одного вида может "эволюционировать" в другого. Так, например, Бульбазавр превращается в Ивизавра, а тот превращается в Венузавра.

![bulba evolution](https://dvmn.org/filer/canonical/1562265973/167/)

### Как запустить

- Скачайте код
- Установите зависимости командой `pip install -r requirements.txt`
- Запустите сервер командой `python3 manage.py runserver`

### Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `manage.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны 2 переменные:
- `DEBUG` — дебаг-режим. Поставьте True, чтобы увидеть отладочную информацию в случае ошибки.
- `SECRET_KEY` — секретный ключ проекта

### Работаем с базой покемонов

Сайт будет доступен по ссылке [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
Чтобы информация о покемонах отобразилась на карте - их надо внести в базу данных.
Наполнение базы данных идет через [Панель администратора](http://127.0.0.1:8000/admin) Django, где:
  - **Pokemons** - список всех покемонов. Каждый экземпляр добавляем через **Add** и сохраняем через **Save**.
    Обязательные поля: **Название** и **Картинка** (чтобы было что отображать на карте), но чем больше информации будет внесено, тем больше шансов на удачную рыбалку.
  - **Pokemon entitys** - список событий, где и когда покемона можно поймать.
    Обязательные поля: **Покемон**, **Широта и Долгота**, **Время появления и исчезновения**  (без этих данных событие теряет смысл), но может повезти и будут дополнительные данные как Защита, Здоровье и т.д.
    Добавляем и сохраняем событие - аналогично.

Не забудьте [Создать суперпользователя](https://developer.mozilla.org/ru/docs/Learn/Server-side/Django/Admin_site#%D0%A1%D0%BE%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5_%D1%81%D1%83%D0%BF%D0%B5%D1%80%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8F) для доступа к Панели администратора Django.

## Цели проекта

Код написан в учебных целях — это урок 4 в курсе Django ORM.

Спасибо [Devman](https://dvmn.org) и счастливой вам охоты...
