# Recurrent
Recurrent - это python библиотека для парсинга повторяющихся событий и дат использующая обработку естественного языка. Rurumi - это перевод оригинальной библиотеки на русский
recurrent обращает строки типа «каждый вторник и четверг до конца этого месяца» в [RFC-compliant RRULES][1], для совмещения с календарем или [python-dateutil's][2]
rrulestr.  It will also accept such rrules and return a natural language representation of them.

```sh
pip install recurrent
```

## примеры
### конкретные даты
* в следующий вторник 
* завтра
* в течение часа
* через 15 минут
* 4 марта в 9 утра
* 3 четверг апреля в 10 часов
* на 40 день 2020 года

### повторяющиеся события
* в будни
* каждрое четвертое число месяца начиная с первого января 2010 и заканчивая 25 декабря 2020
* каждый вторник до следующего месяца месяца
* раз в год в четвертый четверг ноября
* по вторникам и четвергам в 15:15
* по средам в 9 часов
* по пятницам в 11
* ежедневно за исключением июня
* ежедневно за исключением 23 июня и 4 июля
* каждый понедельник кроме второго понедельника в марте
* дважды по пятницам
* трижды в пятницу
* через пятницу 5 раз
* каждые три пятницы с ноября по февраль
* по пятницам начиная с мая по 10 повторений
* по вторникам на протяжении следующих шести недель
* каждый пн-ср на протяжении следующих двух месяцев
* пн-вт-ср со следующего года
* через каждую пятницу в течение следующих трех лет
* каждую первую и последнюю среду и пятницу месяца
* каждый вт и пт на 14 нед
* каждый год 25 дек

### привычные выражения
* назначь встречу на любой вторник в полдень
* поставь напоминание на следующий вторник на 11 вечера

## использование
```python
>>> import datetime
>>> from recurrent.event_parser import RecurringEvent
>>> r = RecurringEvent(now_date=datetime.datetime(2010, 1, 1))
>>> r.parse('каждый день до конца февраля')
'DTSTART:20100105\nRRULE:FREQ=DAILY;INTERVAL=1;UNTIL=20100201'
>>> r.is_recurring
True
>>> r.get_params()
{'dtstart': '20100105', 'freq': 'daily', 'interval': 1, 'until': '20100201'}

>>> r.parse('feb 2nd')
datetime.datetime(2010, 2, 2, 0, 0)

>>> r.parse('not a date at all')

>>> r.format('DTSTART:20100105\nRRULE:FREQ=DAILY;INTERVAL=1;UNTIL=20100201')
'daily from Tue Jan 5, 2010 to Mon Feb 1, 2010'
>>> r.format(r.parse('fridays twice'))
'every Fri twice'
>>>
```

можно использовать python-dateutil чтобы работать с повторениями ^_^
```python
>>> from dateutil import rrule
>>> rr = rrule.rrulestr(r.get_RFC_rrule())
>>> rr.after(datetime.datetime(2010, 1, 2))
datetime.datetime(2010, 1, 5, 0, 0)
>>> rr.after(datetime.datetime(2010, 1, 25))
datetime.datetime(2010, 1, 26, 0, 0)
```

и еще вы можно настроить регион для смены формата `parsedatetime`
```python
consts = parsedatetime.Constants(localeID='en_US', usePyICU=False)
consts.use24 = True

r = RecurringEvent(now_date=datetime.datetime(2010, 1, 1), parse_constants=consts)
```

## Dependencies
Recurrent использует [parsedatetime][3] для парсинга дат и [python.dateutil][2] (если доступно) для оптимизации некоторых результатов

## кредиты
Recurrent вдохновлен похожей библиотекой на Ruby - Tickle от Joshua
Lippiner, которая так же использует parsedatetime для естественного «человечного» перевода.

хендлеры COUNT, BYSETPOS, BYWEEKNO, EXDATE и EXRULE,
а так же форматирование функций реализовано при участии Joe Cool snoopyjc@gmail.com 
https://github.com/snoopyjc

## автор
Ken Van Haren [@squaredloss](http://twitter.com/squaredloss)

[1]: http://www.kanzaki.com/docs/ical/rrule.html
[2]: https://pypi.org/project/python-dateutil
[3]: https://github.com/bear/parsedatetime
[4]: https://github.com/kvh/parsedatetime
