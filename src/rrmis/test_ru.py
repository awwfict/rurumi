# русские тесты rurumi
# каждая строка: (фраза, ожидаемый результат). сейчас = пятница, 1 января 2010
# повторение -> строка RRULE, одна дата -> datetime
import unittest
import datetime
from datetime import datetime as dt

from rrmis.event_parser import RecurringEvent
from rrmis.ru import translate

NOW = datetime.datetime(2010, 1, 1)

expressions = [
    # дни недели: полные слова, сокращения, падежи, регистр
    ('каждый понедельник', 'RRULE:BYDAY=MO;INTERVAL=1;FREQ=WEEKLY'),
    ('каждый вторник', 'RRULE:BYDAY=TU;INTERVAL=1;FREQ=WEEKLY'),
    ('каждую среду', 'RRULE:BYDAY=WE;INTERVAL=1;FREQ=WEEKLY'),
    ('Каждую Среду', 'RRULE:BYDAY=WE;INTERVAL=1;FREQ=WEEKLY'),
    ('каждый четверг', 'RRULE:BYDAY=TH;INTERVAL=1;FREQ=WEEKLY'),
    ('каждую пятницу', 'RRULE:BYDAY=FR;INTERVAL=1;FREQ=WEEKLY'),
    ('каждую субботу', 'RRULE:BYDAY=SA;INTERVAL=1;FREQ=WEEKLY'),
    ('каждое воскресенье', 'RRULE:BYDAY=SU;INTERVAL=1;FREQ=WEEKLY'),
    ('каждый пн', 'RRULE:BYDAY=MO;INTERVAL=1;FREQ=WEEKLY'),
    ('каждую ср', 'RRULE:BYDAY=WE;INTERVAL=1;FREQ=WEEKLY'),
    ('каждое вс', 'RRULE:BYDAY=SU;INTERVAL=1;FREQ=WEEKLY'),
    ('каждый вторник и четверг', 'RRULE:BYDAY=TU,TH;INTERVAL=1;FREQ=WEEKLY'),
    ('каждый понедельник и пятницу в 10:00', 'RRULE:BYDAY=MO,FR;BYHOUR=10;BYMINUTE=0;INTERVAL=1;FREQ=WEEKLY'),

    # «по понедельникам», будни, выходные
    ('по понедельникам', 'RRULE:BYDAY=MO;INTERVAL=1;FREQ=WEEKLY'),
    ('по средам и пятницам', 'RRULE:BYDAY=WE,FR;INTERVAL=1;FREQ=WEEKLY'),
    ('по вторникам и четвергам', 'RRULE:BYDAY=TU,TH;INTERVAL=1;FREQ=WEEKLY'),
    ('по будням', 'RRULE:BYDAY=MO,TU,WE,TH,FR;INTERVAL=1;FREQ=WEEKLY'),
    ('по выходным', 'RRULE:BYDAY=SA,SU;INTERVAL=1;FREQ=WEEKLY'),
    ('в будни', 'RRULE:BYDAY=MO,TU,WE,TH,FR;INTERVAL=1;FREQ=WEEKLY'),
    ('в выходные', 'RRULE:BYDAY=SA,SU;INTERVAL=1;FREQ=WEEKLY'),
    ('каждый будний день', 'RRULE:BYDAY=MO,TU,WE,TH,FR;INTERVAL=1;FREQ=WEEKLY'),

    # частота
    ('ежедневно', 'RRULE:INTERVAL=1;FREQ=DAILY'),
    ('каждый день', 'RRULE:INTERVAL=1;FREQ=DAILY'),
    ('еженедельно', 'RRULE:INTERVAL=1;FREQ=WEEKLY'),
    ('каждую неделю', 'RRULE:INTERVAL=1;FREQ=WEEKLY'),
    ('ежемесячно', 'RRULE:INTERVAL=1;FREQ=MONTHLY'),
    ('каждый месяц', 'RRULE:INTERVAL=1;FREQ=MONTHLY'),
    ('ежегодно', 'RRULE:INTERVAL=1;FREQ=YEARLY'),
    ('каждый год', 'RRULE:INTERVAL=1;FREQ=YEARLY'),
    ('каждый час', 'RRULE:INTERVAL=1;FREQ=HOURLY'),
    ('каждые 30 минут', 'RRULE:INTERVAL=30;FREQ=MINUTELY'),

    # интервал
    ('каждые 3 дня', 'RRULE:INTERVAL=3;FREQ=DAILY'),
    ('каждые два дня', 'RRULE:INTERVAL=2;FREQ=DAILY'),
    ('каждый второй день', 'RRULE:INTERVAL=2;FREQ=DAILY'),
    ('через день', 'RRULE:INTERVAL=2;FREQ=DAILY'),
    ('раз в неделю', 'RRULE:INTERVAL=1;FREQ=WEEKLY'),
    ('раз в две недели', 'RRULE:INTERVAL=2;FREQ=WEEKLY'),
    ('раз в 2 недели', 'RRULE:INTERVAL=2;FREQ=WEEKLY'),
    ('каждую вторую неделю', 'RRULE:INTERVAL=2;FREQ=WEEKLY'),
    ('каждые 2 недели по понедельникам и четвергам', 'RRULE:BYDAY=MO,TH;INTERVAL=2;FREQ=WEEKLY'),

    # время
    ('каждый вторник в 15:00', 'RRULE:BYDAY=TU;BYHOUR=15;BYMINUTE=0;INTERVAL=1;FREQ=WEEKLY'),
    ('каждый вторник в 15:30 до 5 мая', 'RRULE:BYDAY=TU;BYHOUR=15;BYMINUTE=30;INTERVAL=1;FREQ=WEEKLY;UNTIL=20100505'),
    ('каждый вторник в 9 утра', 'RRULE:BYDAY=TU;BYHOUR=9;BYMINUTE=0;INTERVAL=1;FREQ=WEEKLY'),
    ('каждый вторник в 7 вечера', 'RRULE:BYDAY=TU;BYHOUR=19;BYMINUTE=0;INTERVAL=1;FREQ=WEEKLY'),
    ('каждый вторник в 3 дня', 'RRULE:BYDAY=TU;BYHOUR=15;BYMINUTE=0;INTERVAL=1;FREQ=WEEKLY'),
    ('каждый день в 10 часов', 'RRULE:BYHOUR=10;BYMINUTE=0;INTERVAL=1;FREQ=DAILY'),
    ('каждый день в полдень', 'RRULE:BYHOUR=12;BYMINUTE=0;INTERVAL=1;FREQ=DAILY'),
    ('каждый день в 10.05', 'RRULE:BYHOUR=10;BYMINUTE=5;INTERVAL=1;FREQ=DAILY'),

    # начало и конец повторения
    ('каждую среду до 5 мая', 'RRULE:BYDAY=WE;INTERVAL=1;FREQ=WEEKLY;UNTIL=20100505'),
    ('каждую среду до мая', 'RRULE:BYDAY=WE;INTERVAL=1;FREQ=WEEKLY;UNTIL=20100501'),
    ('каждый день до 31.03', 'RRULE:INTERVAL=1;FREQ=DAILY;UNTIL=20100331'),
    ('каждый вторник и четверг до конца этого месяца', 'RRULE:BYDAY=TU,TH;INTERVAL=1;FREQ=WEEKLY;UNTIL=20100131'),
    ('каждый день с 1 марта по 10 марта', 'DTSTART:20100301\nRRULE:INTERVAL=1;FREQ=DAILY;UNTIL=20100310'),
    ('каждый день начиная с 1 марта', 'DTSTART:20100301\nRRULE:INTERVAL=1;FREQ=DAILY'),
    ('каждый день с 1 марта', 'DTSTART:20100301\nRRULE:INTERVAL=1;FREQ=DAILY'),

    # количество и исключения
    ('каждый день 3 раза', 'RRULE:INTERVAL=1;FREQ=DAILY;COUNT=3'),
    ('каждый день дважды', 'RRULE:INTERVAL=1;FREQ=DAILY;COUNT=2'),
    ('каждый понедельник 5 раз', 'RRULE:BYDAY=MO;INTERVAL=1;FREQ=WEEKLY;COUNT=5'),
    ('ежедневно кроме 8 марта', 'RRULE:INTERVAL=1;FREQ=DAILY\nEXDATE:20100308T000000'),
    ('каждый день кроме выходных', 'RRULE:INTERVAL=1;FREQ=DAILY\nEXRULE:BYDAY=SA,SU;INTERVAL=1;FREQ=WEEKLY'),
    ('каждый день за исключением выходных', 'RRULE:INTERVAL=1;FREQ=DAILY\nEXRULE:BYDAY=SA,SU;INTERVAL=1;FREQ=WEEKLY'),

    # дни месяца и года
    ('каждый первый понедельник месяца', 'RRULE:BYDAY=1MO;INTERVAL=1;FREQ=MONTHLY'),
    ('первый понедельник каждого месяца', 'RRULE:BYDAY=1MO;INTERVAL=1;FREQ=MONTHLY'),
    ('каждую последнюю пятницу месяца', 'RRULE:BYDAY=-1FR;INTERVAL=1;FREQ=MONTHLY'),
    ('каждый последний день месяца', 'RRULE:BYMONTHDAY=-1;INTERVAL=1;FREQ=MONTHLY'),
    ('в последний день каждого месяца', 'RRULE:BYMONTHDAY=-1;INTERVAL=1;FREQ=MONTHLY'),
    ('каждое 12 число', 'RRULE:BYMONTHDAY=12;INTERVAL=1;FREQ=MONTHLY'),
    ('каждый месяц 12 числа', 'RRULE:BYMONTHDAY=12;INTERVAL=1;FREQ=MONTHLY'),
    ('каждые 2 месяца 5 числа', 'RRULE:BYMONTHDAY=5;INTERVAL=2;FREQ=MONTHLY'),
    ('каждое 12 марта', 'RRULE:BYMONTHDAY=12;BYMONTH=3;INTERVAL=1;FREQ=YEARLY'),
    ('каждый год 12 марта', 'RRULE:BYMONTHDAY=12;BYMONTH=3;INTERVAL=1;FREQ=YEARLY'),
    ('ежегодно 12 марта', 'RRULE:BYMONTHDAY=12;BYMONTH=3;INTERVAL=1;FREQ=YEARLY'),
    ('каждый сент', 'RRULE:BYMONTH=9;INTERVAL=1;FREQ=YEARLY'),

    # одна дата (не повторение)
    ('12 марта', dt(2010, 3, 12, 0, 0)),
    ('12 марта 2027', dt(2027, 3, 12, 0, 0)),
    ('12-го марта', dt(2010, 3, 12, 0, 0)),
    ('12.03', dt(2010, 3, 12, 0, 0)),
    ('12.03.2027', dt(2027, 3, 12, 0, 0)),
    ('5.05 в 18:00', dt(2010, 5, 5, 18, 0)),
    ('завтра', dt(2010, 1, 2, 9, 0)),
    ('завтра в 15:00', dt(2010, 1, 2, 15, 0)),
    ('послезавтра', dt(2010, 1, 3, 0, 0)),
    ('сегодня в 18:00', dt(2010, 1, 1, 18, 0)),
    ('в 15.30', dt(2010, 1, 1, 15, 30)),
    ('в пятницу', dt(2010, 1, 8, 0, 0)),
    ('в следующий вторник', dt(2010, 1, 5, 9, 0)),
    ('через 3 дня', dt(2010, 1, 4, 0, 0)),
    ('через неделю', dt(2010, 1, 8, 0, 0)),
    ('через 2 недели', dt(2010, 1, 15, 0, 0)),
    ('последний день месяца', dt(2010, 1, 31, 0, 0)),

    # лишние слова не мешают
    ('встреча каждую среду в 15:00', 'RRULE:BYDAY=WE;BYHOUR=15;BYMINUTE=0;INTERVAL=1;FREQ=WEEKLY'),
    # время в конце фразы, после «до / с / кроме»
    ('каждую среду до 5 мая в 15:00', 'RRULE:BYDAY=WE;BYHOUR=15;BYMINUTE=0;INTERVAL=1;FREQ=WEEKLY;UNTIL=20100505'),
    ('каждый день с 1 марта по 10 марта в 9 утра', 'DTSTART:20100301\nRRULE:BYHOUR=9;BYMINUTE=0;INTERVAL=1;FREQ=DAILY;UNTIL=20100310'),
    ('каждый день начиная с 1 марта в 18:00', 'DTSTART:20100301\nRRULE:BYHOUR=18;BYMINUTE=0;INTERVAL=1;FREQ=DAILY'),
    ('ежедневно кроме выходных в 8:30', 'RRULE:BYHOUR=8;BYMINUTE=30;INTERVAL=1;FREQ=DAILY\nEXRULE:BYDAY=SA,SU;INTERVAL=1;FREQ=WEEKLY'),
    ('по пятницам начиная с мая по 10 повторений в 11', 'DTSTART:20100501\nRRULE:BYDAY=FR;BYHOUR=11;BYMINUTE=0;INTERVAL=1;FREQ=WEEKLY;COUNT=10'),

    # все примеры из readme.md
    ('в следующий вторник', dt(2010, 1, 5, 9, 0)),
    ('завтра', dt(2010, 1, 2, 9, 0)),
    ('через час', dt(2010, 1, 1, 1, 0)),
    ('через 15 минут', dt(2010, 1, 1, 0, 15)),
    ('4 марта в 9 утра', dt(2010, 3, 4, 9, 0)),
    ('3-й четверг апреля в 10 часов', dt(2010, 4, 15, 10, 0)),
    ('на 40 день 2020 года', dt(2020, 2, 9, 0, 0)),
    ('в будни', 'RRULE:BYDAY=MO,TU,WE,TH,FR;INTERVAL=1;FREQ=WEEKLY'),
    ('каждое четвертое число месяца начиная с первого января 2010 и заканчивая 25 декабря 2020', 'DTSTART:20100101\nRRULE:BYMONTHDAY=4;INTERVAL=1;FREQ=MONTHLY;UNTIL=20201225'),
    ('каждый четверг до следующего месяца', 'RRULE:BYDAY=TH;INTERVAL=1;FREQ=WEEKLY;UNTIL=20100201'),
    ('раз в год в четвертый четверг ноября', 'RRULE:BYDAY=4TH;BYMONTH=11;INTERVAL=1;FREQ=YEARLY'),
    ('по вторникам и четвергам в 15:15', 'RRULE:BYDAY=TU,TH;BYHOUR=15;BYMINUTE=15;INTERVAL=1;FREQ=WEEKLY'),
    ('по средам в 9 часов', 'RRULE:BYDAY=WE;BYHOUR=9;BYMINUTE=0;INTERVAL=1;FREQ=WEEKLY'),
    ('по пятницам в 11', 'RRULE:BYDAY=FR;BYHOUR=11;BYMINUTE=0;INTERVAL=1;FREQ=WEEKLY'),
    ('ежедневно за исключением июня', 'RRULE:INTERVAL=1;FREQ=DAILY\nEXDATE:20100601T000000'),
    ('ежедневно за исключением 23 июня и 4 июля', 'RRULE:INTERVAL=1;FREQ=DAILY\nEXDATE:20100623T000000,20100704T000000'),
    ('каждый понедельник кроме второго понедельника в марте', 'RRULE:BYDAY=MO;INTERVAL=1;FREQ=WEEKLY\nEXDATE:20100308T000000'),
    ('по пятницам 2 раза', 'RRULE:BYDAY=FR;INTERVAL=1;FREQ=WEEKLY;COUNT=2'),
    ('по пятницам 3 раза', 'RRULE:BYDAY=FR;INTERVAL=1;FREQ=WEEKLY;COUNT=3'),
    ('через пятницу 5 раз', 'RRULE:BYDAY=FR;INTERVAL=2;FREQ=WEEKLY;COUNT=5'),
    ('каждые три пятницы с ноября по февраль', 'DTSTART:20101101\nRRULE:BYDAY=FR;INTERVAL=3;FREQ=WEEKLY;UNTIL=20110201'),
    ('по пятницам начиная с мая по 10 повторений', 'DTSTART:20100501\nRRULE:BYDAY=FR;INTERVAL=1;FREQ=WEEKLY;COUNT=10'),
    ('по вторникам на протяжении следующих шести недель', 'RRULE:BYDAY=TU;INTERVAL=1;FREQ=WEEKLY;UNTIL=20100212'),
    ('каждый пн-ср на протяжении следующих двух месяцев', 'RRULE:BYDAY=MO,TU,WE;INTERVAL=1;FREQ=WEEKLY;UNTIL=20100301'),
    ('пн-вт-ср в течение следующего года', 'RRULE:BYDAY=MO,TU,WE;INTERVAL=1;FREQ=WEEKLY;UNTIL=20110101'),
    ('через пятницу в течение следующих трех лет', 'RRULE:BYDAY=FR;INTERVAL=2;FREQ=WEEKLY;UNTIL=20130101'),
    ('каждую первую и последнюю среду и пятницу месяца', 'RRULE:BYDAY=WE,FR;BYSETPOS=1,-1;INTERVAL=1;FREQ=MONTHLY'),
    ('каждый вт и пт на 14-й неделе года', 'RRULE:BYDAY=TU,FR;BYWEEKNO=14;INTERVAL=1;FREQ=YEARLY'),
    ('каждый год 25 дек', 'RRULE:BYMONTHDAY=25;BYMONTH=12;INTERVAL=1;FREQ=YEARLY'),
    ('назначь встречу через вторник в полдень', 'RRULE:BYDAY=TU;BYHOUR=12;BYMINUTE=0;INTERVAL=2;FREQ=WEEKLY'),
    ('поставь напоминание на следующий вторник на 11 вечера', dt(2010, 1, 5, 23, 0)),
    ('каждый день начиная со следующего вторника до февраля', 'DTSTART:20100105\nRRULE:INTERVAL=1;FREQ=DAILY;UNTIL=20100201'),
]

# слова, которые НЕ должны превращаться в день недели или месяц
not_dates = ['с', 'срочно', 'сразу', 'что', 'все', 'встреча', 'сбор', 'птица', 'втроем',
             'майка', 'декада', 'мартышка', 'марка']
DATE_WORDS = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
              'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
              'september', 'october', 'november', 'december')


class RussianTest(unittest.TestCase):

    def test_expressions(self):
        for text, expected in expressions:
            with self.subTest(text=text):
                r = RecurringEvent(now_date=NOW)
                self.assertEqual(r.parse(text), expected)

    def test_not_dates(self):
        for word in not_dates:
            with self.subTest(word=word):
                for date_word in DATE_WORDS:
                    self.assertNotIn(date_word, translate(word).split())

    def test_english_untouched(self):
        self.assertEqual(translate('every monday at 3pm'), 'every monday at 3pm')


if __name__ == '__main__':
    unittest.main()