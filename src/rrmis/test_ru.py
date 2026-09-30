# русские тесты rurumi
# каждая строка: (фраза, ожидаемый RRULE). None — фраза не должна распознаваться
import unittest
import datetime

from rrmis.event_parser import RecurringEvent

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

    # «по понедельникам», будни, выходные
    ('по понедельникам', 'RRULE:BYDAY=MO;INTERVAL=1;FREQ=WEEKLY'),
    ('по средам', 'RRULE:BYDAY=WE;INTERVAL=1;FREQ=WEEKLY'),
    ('по будням', 'RRULE:BYDAY=MO,TU,WE,TH,FR;INTERVAL=1;FREQ=WEEKLY'),
    ('по выходным', 'RRULE:BYDAY=SA,SU;INTERVAL=1;FREQ=WEEKLY'),

    # частота
    ('ежедневно', 'RRULE:INTERVAL=1;FREQ=DAILY'),
    ('каждый день', 'RRULE:INTERVAL=1;FREQ=DAILY'),
    ('еженедельно', 'RRULE:INTERVAL=1;FREQ=WEEKLY'),
    ('каждую неделю', 'RRULE:INTERVAL=1;FREQ=WEEKLY'),
    ('ежемесячно', 'RRULE:INTERVAL=1;FREQ=MONTHLY'),
    ('каждый месяц', 'RRULE:INTERVAL=1;FREQ=MONTHLY'),
    ('ежегодно', 'RRULE:INTERVAL=1;FREQ=YEARLY'),
    ('каждый год', 'RRULE:INTERVAL=1;FREQ=YEARLY'),

    # интервал: цифрой и словом
    ('каждые 3 дня', 'RRULE:INTERVAL=3;FREQ=DAILY'),
    ('каждые два дня', 'RRULE:INTERVAL=2;FREQ=DAILY'),

    # месяцы: сокращения не должны ломаться
    ('каждый сент', 'RRULE:BYMONTH=9;INTERVAL=1;FREQ=YEARLY'),
]

# слова, которые НЕ должны считаться днём недели или месяцем
not_dow = ['с', 'срочно', 'сразу', 'что', 'все', 'встреча', 'сбор', 'птица', 'втроём']
not_moy = ['майка', 'декада', 'мартышка', 'марка']


class RussianTest(unittest.TestCase):

    def test_expressions(self):
        for text, expected in expressions:
            with self.subTest(text=text):
                r = RecurringEvent(now_date=NOW)
                self.assertEqual(r.parse(text), expected)

    def test_not_dow(self):
        from rrmis.constants import RE_DOW
        for word in not_dow:
            with self.subTest(word=word):
                self.assertIsNone(RE_DOW.match(word))

    def test_not_moy(self):
        from rrmis.constants import RE_MOY
        for word in not_moy:
            with self.subTest(word=word):
                self.assertIsNone(RE_MOY.match(word))


if __name__ == '__main__':
    unittest.main()
