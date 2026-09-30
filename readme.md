# 💟 Rurumi
Rurumi - это перевод и адаптация проекта [Recurrent](https://github.com/kvh/recurrent) — англоязычного парсера, созданного для обработки событий с повторениями。 его оригинальный README сохранен и доступен [вот здесь!](en_readme.md)

> ☘️ русские фразы поддерживаются! обратное описание (`format`) пока возвращает текст на английском。

Rurumi обращает строки типа «каждый вторник и четверг до конца этого месяца» в [RFC-compliant RRULES][1], для совмещения с календарем или [python-dateutil's][2] rrulestr。 а так же принимает такие rrules и возвращает их описание на естественном языке。

```sh
pip install git+https://github.com/awwfict/rurumi
```

## 👀 наглядно
### конкретные даты
* в следующий вторник 
* завтра
* через час
* через 15 минут
* 4 марта в 9 утра
* 3-й четверг апреля в 10 часов
* на 40 день 2020 года

### повторяющиеся события
* в будни
* каждое четвертое число месяца начиная с первого января 2010 и заканчивая 25 декабря 2020
* каждый четверг до следующего месяца
* раз в год в четвертый четверг ноября
* по вторникам и четвергам в 15:15
* по средам в 9 часов
* по пятницам в 11
* ежедневно за исключением июня
* ежедневно за исключением 23 июня и 4 июля
* каждый понедельник кроме второго понедельника в марте
* по пятницам 2 раза
* по пятницам 3 раза
* через пятницу 5 раз
* каждые три пятницы с ноября по февраль
* по пятницам начиная с мая по 10 повторений
* по вторникам на протяжении следующих шести недель
* каждый пн-ср на протяжении следующих двух месяцев
* пн-вт-ср в течение следующего года
* через пятницу в течение следующих трех лет
* каждую первую и последнюю среду и пятницу месяца
* каждый вт и пт на 14-й неделе года
* каждый год 25 дек

### привычные выражения
* назначь встречу через вторник в полдень
* поставь напоминание на следующий вторник на 11 вечера

## 🛠️ как использовать
```python
>>> import datetime
>>> from rrmis.event_parser import RecurringEvent
>>> r = RecurringEvent(now_date=datetime.datetime(2010, 1, 1))
>>> r.parse('каждый день начиная со следующего вторника до февраля')
'DTSTART:20100105\nRRULE:FREQ=DAILY;INTERVAL=1;UNTIL=20100201'
>>> r.is_recurring
True
>>> r.get_params()
{'dtstart': '20100105', 'freq': 'daily', 'interval': 1, 'until': '20100201'}

>>> r.parse('2 февраля')
datetime.datetime(2010, 2, 2, 0, 0)

>>> r.parse('это вообще не дата')

>>> r.format('DTSTART:20100105\nRRULE:FREQ=DAILY;INTERVAL=1;UNTIL=20100201')
'daily from Tue Jan 5, 2010 to Mon Feb 1, 2010'
>>> r.format(r.parse('по пятницам дважды'))
'every Fri twice'
>>>
```
можно добавить python-dateutil чтобы работать с повторениями ^_^ ::
```python
>>> from dateutil import rrule
>>> rr = rrule.rrulestr(r.get_RFC_rrule())
>>> rr.after(datetime.datetime(2010, 1, 2))
datetime.datetime(2010, 1, 5, 0, 0)
>>> rr.after(datetime.datetime(2010, 1, 25))
datetime.datetime(2010, 1, 26, 0, 0)
```

и еще в дополнение к вышесказанному можно настроить регион для смены формата `parsedatetime`:
```python
consts = parsedatetime.Constants(localeID='ru_RU', usePyICU=False)
consts.use24 = True

r = RecurringEvent(now_date=datetime.datetime(2010, 1, 1), parse_constants=consts)
```

## 🤓 как это устроено
русская фраза сначала переводится в английскую (`src/rrmis/ru.py`), а дальше её разбирает оригинальный парсер Recurrent:
```
каждую среду до 5 мая в 15:00  →  every wednesday until may 5 at 15:00  →  RRULE:BYDAY=WE;BYHOUR=15;BYMINUTE=0;INTERVAL=1;FREQ=WEEKLY;UNTIL=20100505
```
падежи приводятся к начальной форме с помощью [pymorphy3][5]。

### константы в `ru.py`
`constants.py` оставлен как в оригинале, чтобы английский парсер работал без изменений。 русские списки лежат в `ru.py`, и у некоторых из них свои названия:

| в `ru.py` | аналог в `constants.py` | что это |
|---|---|---|
| `holis` | `DoWs` | дни недели + будни и выходные。 номер строки = день, порядок не менять |
| `RE_holis` | `RE_DOWS` | те же дни, готовые к поиску в тексте |
| `monblans` | `MoYs` | месяцы с января по декабрь。 номер строки + 1 = номер месяца |
| `RE_monblans` | `RE_MOYS` | те же месяцы, готовые к поиску |
| `holis_en`, `monblans_en` | — | английские названия в том же порядке, по ним русское слово переводится для парсера |
| `numbers`, `ordinals` | `numbers`, `ordinals` | числительные: «два» → 2, «третий» → third |
| `ABBREVIATIONS` | — | сокращения, которые pymorphy3 портит («мин», «сек») |
| `WORDS` | — | остальные слова: «каждый» → every, «до» → until… |
| `PHRASES` | — | фразы из нескольких слов: «раз в неделю», «в 9 утра», «до конца месяца»。 порядок важен |

## 🐟 зависимости
Rurumi, как и Recurrent, использует [parsedatetime][3] для парсинга дат и [python.dateutil][2] (если доступно) для оптимизации некоторых результатов。 для русских падежей используется [pymorphy3][5]。

---

## 💕 благодарности
Recurrent вдохновлен похожей Ruby-библиотекой _Tickle_ от _Joshua Lippiner_, которая так же использует parsedatetime для естественного «человечного» распознавания。

хендлеры COUNT, BYSETPOS, BYWEEKNO, EXDATE и EXRULE,а так же функции форматирования реализованы при участии Joe Cool snoopyjc@gmail.com 
https://github.com/snoopyjc !

## 🪪 автор
Ken Van Haren [@squaredloss](http://twitter.com/squaredloss)

[1]: http://www.kanzaki.com/docs/ical/rrule.html
[2]: https://pypi.org/project/python-dateutil
[3]: https://github.com/bear/parsedatetime
[4]: https://github.com/kvh/parsedatetime
[5]: https://pypi.org/project/pymorphy3
