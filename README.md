# Разработка системы с web-интерфейсом для сопоставления характеристик товаров маркетплейса с их эталонными значениями

> Команда: ***i plow()***
>
> Кейс решён в рамках хакатона [AgoraHack2022](https://hackathon.agora.ru/)
---

## Оглавление

1. [Задача](#Постановка-задачи)
2. [Алгоритм](#Алгоритм)
3. [Результаты](#Результаты)
4. [Улучшения](#Как-мы-улучшали-качество-матчинга)
5. [Дополнительные фичи](#Дополнительные-фичи)
6. [Наш Стек](#Стек)
7. [Как запустить?](#Как-запустить?)
8. [i plow()](#i-plow---это-мы)

## Постановка задачи

Дана база товаров со следующими полями.

| Поле           | Инфо                                                           |
| -------------- | -------------------------------------------------------------- |
| `name`         | Наименование товара                                            |
| `is_reference` | True, если товар является эталоном. Тогда reference_id "None". |
| `product_id`   | id продукта                                                    |
| `reference_id` | id эталона для этого продукта                                  |
| `props`        | массив строк-свойств товара                                    |

В ней имеются как товары-эталоны (471 шт.), так и товары продавцов (2780 шт.)

Основываясь на этих данных необходимо разработать микросервис, сопостовляющий товары продавцов с эталонами. Взаимодействие с сервисом должно осуществляться посредством отправки POST запроса с JSON-массивом, содержащим товары. Ответ сервиса должен состоять из id эталонов для каждого товара.

## Алгоритм

Для матчинга поступающего на вход сервису товара мы выполняем следующие действия:

1. Отдаем название товара в MongoDB - перед поиском он автоматически производит лемматизацию названия.
2. Затем  производится полнотекстовый поиск по названию товара по имеющимся эталонам, чтобы найти схожие.
3. После мы выбираем эталон с наибольшим textScore и возвращаем его id.

## Результаты

Для оценки результатов работы нашего алгоритма в качестве метрики мы выбрали Accuracy.

`Accuracy = Количество верно предсказанных эталоннов / Количество предсказаний`

Чтобы замерить скорость работы алгоритма, мы отправляли ему батчи по 100, 1000, 2780

| Кол-во товаров | Время работы (с) | Время на 100 товаров (с) | Accuracy |
| -------------- | ---------------- | ------------------------ | -------- |
| 100            | 0.2715           | 0.2715                   | 0.8800   |
| 1000           | 1.6553           | 0.1655                   | 0.8840   |
| 2780           | 4.7229           | 0.1698                   | 0.8996   |



## Как мы улучшали качество матчинга

1. Провели лемматизацию именований у эталонов.
2. (WIP) Разделили и добавили по частям именования со спецсимволами. (Было "сплит-система", стало "сплит-система сплит система")
3. (WIP) Думаем над тем как использовать свойства товаров.

## Дополнительные фичи

- Набор методов для интеграции системы пользовательских прав.
- Оперирование данными - Набор методов для добавления новых данных.
- Простота использования - Интерактивная документация, позволяющая "пощупать" API с помощью web-интерфейса.
- Простота интеграции - Контейнеризация микросервиса с помощью Docker, позволяющая без лишних усилий интегрировать его в рабочий процесс.
- Безграничная масштабируемость - нет необходимости переобучать модель при добавлении новых эталонов


## Наш Стек

- [Python](https://www.python.org/) - основной язык
- [FastApi](https://fastapi.tiangolo.com/) - Rest/API
- [pymystem3](https://yandex.ru/dev/mystem/) - лемматизация эталонов
- [MongoDB](https://www.mongodb.com/) - хранение и поиск по эталонам
- [PostgreSQL](https://www.postgresql.org/?&) - хранение информации о пользователях
- [Docker, docker-compose](https://www.docker.com/) - контейнеризация

## Как запустить?

WIP

## i plow() - это мы

>- Голубев Егор - бекенд-разработчик
>- Тампио Илья - ML-специалист
>- Лернер Роман - Product менеджер
>- Молоткова Ника - UI/UX дизайнер
>- Лебедева Татьяна - Frontend-разработчик