# rurumi: перевод русской фразы в английскую, которую понимает парсер recurrent
#
# как это работает:
#   1. каждое слово приводится к начальной форме (pymorphy3): «среду» -> «среда», «марта» -> «март»
#   2. дни недели и месяцы узнаются по спискам holis и monblans (с сокращениями)
#   3. фразы («раз в неделю», «до конца месяца», «в 9 утра») заменяются английскими
#   4. оставшиеся слова переводятся по словарю WORDS, незнакомые русские слова выбрасываются
#
# пример: «каждую среду до 5 мая в 15:00» -> «every wednesday until may 5 at 15:00»

import re

import pymorphy3

morph = pymorphy3.MorphAnalyzer()   # создаётся один раз: загрузка словаря медленная


# дни недели: номер строки = день, порядок не менять
holis = (
    r'(понедельник)|(пн)',
    r'вт(орник)?',
    r'ср(еда)?',
    r'(четверг)|(чт)',
    r'(пт)|(пятница)',
    r'(сб)|субб(ота)?',
    r'(вс)|воскресен(ье|ие)?',
    r'будни',
    r'выходн(ой|ые)',
)
RE_holis = [re.compile(r) for r in holis]
holis_en = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
            'weekdays', 'weekends')

# месяцы: номер строки + 1 = номер месяца, порядок не менять
monblans = (
    r'янв(арь)?',
    r'фев(р(аль)?)?',
    r'март',
    r'апр(ель)?',
    r'май',
    r'июнь',
    r'июль',
    r'авг(уст)?',
    r'сент?(ябрь)?',
    r'окт(ябрь)?',
    r'нояб(рь)?',
    r'дек(абрь)?',
)
RE_monblans = [re.compile(r) for r in monblans]
monblans_en = ('january', 'february', 'march', 'april', 'may', 'june', 'july',
               'august', 'september', 'october', 'november', 'december')

# сокращения, которые pymorphy3 портит («мин» -> «мина», «сек» -> «сечь»)
ABBREVIATIONS = {
    'мин': 'minute',
    'сек': 'second',
    'ч': 'hour',
}

# количественные числительные -> цифры
numbers = {
    'ноль': 0, 'один': 1, 'два': 2, 'три': 3, 'четыре': 4, 'пять': 5,
    'шесть': 6, 'семь': 7, 'восемь': 8, 'девять': 9, 'десять': 10,
    'одиннадцать': 11, 'двенадцать': 12, 'пятнадцать': 15, 'двадцать': 20, 'тридцать': 30,
}

# порядковые числительные
ordinals = {
    'первый': 'first', 'второй': 'second', 'третий': 'third', 'четвертый': 'fourth',
    'пятый': 'fifth', 'шестой': 'sixth', 'седьмой': 'seventh', 'восьмой': 'eighth',
    'девятый': 'ninth', 'десятый': 'tenth', 'последний': 'last',
}

# остальные слова (в начальной форме)
WORDS = {
    'каждый': 'every', 'всякий': 'every',
    'ежедневно': 'daily', 'еженедельно': 'weekly', 'ежемесячно': 'monthly',
    'ежегодно': 'yearly', 'ежечасно': 'hourly',
    'день': 'day', 'неделя': 'week', 'месяц': 'month', 'год': 'year',
    'час': 'hour', 'минута': 'minute', 'секунда': 'second',
    'и': 'and', 'или': 'or',
    'сегодня': 'today', 'завтра': 'tomorrow', 'послезавтра': 'in 2 days',
    'следующий': 'next', 'этот': 'this', 'это': 'this', 'прошлый': 'last',
    'до': 'until', 'кроме': 'except',
    'дважды': 'twice', 'трижды': '3 times',
}

DAYS = '|'.join(holis_en[:7])
MONTHS = '|'.join(monblans_en)
UNITS = 'день|неделя|месяц|год|час|минута'

# фразы: (регулярка по словам в начальной форме, замена). порядок важен
ORDINAL_WORDS = '|'.join(list(ordinals.values())[:10])
PLURAL_UNITS = {'день': 'days', 'неделя': 'weeks', 'месяц': 'months', 'год': 'years'}
ORDINAL_NUMBERS = {w: i + 1 for i, w in enumerate(list(ordinals.values())[:10])}

PHRASES = [
    # «через день» — повторение, «через 3 дня» — одна дата, «через пятницу» — каждую вторую пятницу
    (r'\bчерез день\b', 'every other day'),
    # «пн-ср в течение года» без «каждый» — всё равно повторение
    (r'^(%s) thru (%s)\b' % (DAYS, DAYS), r'every \1 thru \2'),
    (r'\bчерез (%s)\b' % DAYS, r'every other \1'),
    (r'\bчерез (\d+) (%s)\b' % UNITS, r'in \1 \2'),
    (r'\bчерез (%s)\b' % UNITS, r'in 1 \1'),

    # «раз в неделю», «раз в 2 недели»
    (r'\bраз в (\d+) (%s)\b' % UNITS, r'every \1 \2'),
    (r'\bраз в (%s)\b' % UNITS, r'every \1'),

    # «3 раза», «5 раз», «по 10 повторений»
    (r'\b(\d+) раз\b', r'\1 times'),
    (r'\b(?:по )?(\d+) повторение\b', r'for \1 occurrences'),

    # «в течение следующих 6 недель», «на протяжении следующего года»
    (r'\b(?:в течение|на протяжение) следующий (\d+) (день|неделя|месяц|год)\b',
     lambda m: 'for the next %s %s' % (m.group(1), PLURAL_UNITS[m.group(2)])),
    (r'\b(?:в течение|на протяжение) следующий (неделя|месяц|год)\b',
     lambda m: 'for the next ' + {'неделя': 'week', 'месяц': 'month', 'год': 'year'}[m.group(1)]),

    # «на 14-й неделе года» -> «in week 14»
    (r'\b(?:на|в) (\d+)(?:st|nd|rd|th)? неделя(?: год)?\b', r'in week \1'),

    # «на 40 день 2020 года» -> «40th day of 2020»
    (r'\b(?:на |в )?(\d+)(?:st|nd|rd|th)? день (\d{4})(?: год)?\b',
     lambda m: '%s day of %s' % (english_ordinal(m.group(1)), m.group(2))),

    # «каждый будний день», «по выходным дням»
    (r'\bбудний день\b', 'weekday'),
    (r'\bвыходной день\b', 'weekend'),

    # «первый понедельник месяца», «последняя пятница каждого месяца»
    (r'\b(%s) каждый месяц\b' % DAYS, r'\1 of every month'),
    (r'\b(%s) месяц\b' % DAYS, r'\1 of the month'),
    (r'\blast день месяц\b', 'last day of the month'),

    # время: «в 15:00», «в 9 утра», «на 11 вечера», «в 3 дня», «в 10 часов», «в полдень»
    (r'\b(?:в|на) (\d{1,2}):(\d{2})\b', r'at \1:\2'),
    (r'\b(?:в|на) (\d{1,2}) (утро|ночь)\b', r'at \1am'),
    (r'\b(?:в|на) (\d{1,2}) (вечер|день)\b', r'at \1pm'),
    (r'\b(?:в|на) (\d{1,2}) час\b', r'at \1:00'),
    (r'\bв полдень\b', 'at 12:00'),
    (r'\bв полночь\b', 'at 0:00'),
    (r'(?<!at )(?<!\d)\b(\d{1,2}):(\d{2})\b', r'at \1:\2'),

    # числа месяца: «каждое 12 число», «каждый месяц 12 числа», «каждое четвертое число месяца»
    (r'\bкаждый месяц (\d{1,2})(?:st|nd|rd|th)? число\b', r'every month on the \1th'),
    (r'\bкаждый (\d{1,2})(?:st|nd|rd|th)? число(?: месяц)?\b', r'every month on the \1th'),
    (r'\bкаждый (%s) число(?: месяц)?\b' % ORDINAL_WORDS, r'every \1 of the month'),
    (r'\b(\d{1,2})(?:st|nd|rd|th)? число каждый месяц\b', r'every month on the \1th'),
    (r'\b(\d{1,2})(?:st|nd|rd|th)? число\b', r'the \1th'),

    # даты: «12 марта», «12-го марта 2027», «первого января» -> «march 12», «march 12 2027», «january 1»
    (r'\b(\d{1,2})(?:st|nd|rd|th)? (%s)\b' % MONTHS, r'\2 \1'),
    (r'\b(%s) (%s)\b' % (ORDINAL_WORDS, MONTHS), lambda m: '%s %d' % (m.group(2), ORDINAL_NUMBERS[m.group(1)])),

    # «3-й четверг апреля» -> «3rd thursday in april»
    (r'\b(%s) (%s)\b' % (DAYS, MONTHS), r'\1 in \2'),

    # «каждую первую и последнюю среду и пятницу месяца»
    (r'\bкаждый (%s|last) и (%s|last) (%s) и (%s) of the month\b' % (ORDINAL_WORDS, ORDINAL_WORDS, DAYS, DAYS),
     r'monthly on the \1 and \2 instance of \3 and \4'),

    # «каждое 12 марта», «каждый год 12 марта», «ежегодно 12 марта»
    (r'\bкаждый год ((?:%s) \d{1,2})\b' % MONTHS, r'every year on \1'),
    (r'\bкаждый ((?:%s) \d{1,2})\b' % MONTHS, r'every year on \1'),
    (r'\bежегодно ((?:%s) \d{1,2})\b' % MONTHS, r'yearly on \1'),

    # «до конца этого месяца», «до конца года»
    (r'\bконец (?:этот |это )?(месяц|год|неделя)\b', r'the end of this \1'),

    # «начиная с 1 января и заканчивая 25 декабря»
    (r'\bначинать с (.+?) (?:and )?заканчивать (.+)$', r'from \1 to \2'),
    # «с 1 марта по 10 марта», «с 1 марта до 10 марта»
    (r'\bс (.+?) (?:по|до) (.+)$', r'from \1 to \2'),
    # «начиная с 1 марта», «с понедельника»
    (r'\bначинать с\b', 'starting'),
    (r'\bс (?=(?:%s|%s|\d|tomorrow|today|next|завтра|сегодня|следующий))' % (MONTHS, DAYS), 'starting '),

    # «за исключением»
    (r'\bза исключение\b', 'except'),

    # «по пятницам в 11» — просто час, без минут
    (r'\bв (\d{1,2})\b(?![:.\d])(?! (?:день|неделя|месяц|год|час|минута|times|occurrences))', r'at \1:00'),
]
PHRASES = [(re.compile(p), r) for p, r in PHRASES]

RE_TOKEN = re.compile(r'\d+(?:[:./]\d+)*(?:-[а-я]+)?|[а-яa-z]+|,')
RE_DATE_DOTS = re.compile(r'^(\d{1,2})\.(\d{1,2})(?:\.(\d{4}))?$')
RE_TIME_AFTER_END = re.compile(r'^(.*?)( (?:until|from|starting|except) .*?)( at \d{1,2}(?::\d{2})?(?:am|pm)?)(.*)$')
RE_DAY_RANGE = re.compile(r'\b[а-я]+(?:-[а-я]+)+\b')
RE_DOTTED_TIME = re.compile(r'\bв (\d{1,2})\.(\d{2})\b')
RE_DOTTED_DATE = re.compile(r'(?<!в )(?<!at )\b(\d{1,2})\.(\d{1,2})(?:\.(\d{4}))?\b')
RE_ORDINAL_DIGITS = re.compile(r'^(\d{1,2})-[а-я]+$')
RE_CYRILLIC = re.compile(r'[а-я]')


def english_ordinal(n):
    n = int(n)
    if 10 <= n % 100 <= 20:
        return '%dth' % n
    return '%d%s' % (n, {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th'))


def find(word, regexes, names):
    for i, r in enumerate(regexes):
        if r.fullmatch(word):
            return names[i]
    return None


def translate_word(word):
    # цифры: «12.03.2027» -> «march 12 2027», «12-го» -> «12th», «15:00» — как есть
    if word[0].isdigit():
        m = RE_DATE_DOTS.match(word)
        if m:
            return dotted_date(m)
        m = RE_ORDINAL_DIGITS.match(word)
        if m:
            return english_ordinal(m.group(1))
        return word
    if not RE_CYRILLIC.search(word):
        return word

    # сокращения — до pymorphy3, он их портит
    if word in ABBREVIATIONS:
        return ABBREVIATIONS[word]
    found = find(word, RE_holis, holis_en) or find(word, RE_monblans, monblans_en)
    if found:
        return found

    parse = morph.parse(word)[0]
    lemma = parse.normal_form.replace('ё', 'е')

    # «по понедельникам», «по средам» — множественное число
    day = find(lemma, RE_holis, holis_en)
    if day and day in holis_en[:7] and parse.tag.number == 'plur':
        return day + 's'
    if lemma in ('будни', 'будний') and parse.tag.number == 'plur' and word != 'будний':
        return 'weekdays'
    if lemma == 'выходной' and parse.tag.number == 'plur':
        return 'weekends'

    found = day or find(lemma, RE_monblans, monblans_en)
    if found:
        return found
    if lemma in numbers:
        return str(numbers[lemma])
    if lemma in ordinals:
        return ordinals[lemma]
    return lemma


def day_range(m):
    days = [find(w, RE_holis, holis_en) for w in m.group(0).split('-')]
    if None in days or len(days) < 2:
        return m.group(0)
    return '%s thru %s' % (days[0], days[-1])


def dotted_date(m):
    day, month, year = m.group(1), m.group(2), m.group(3)
    if not 1 <= int(month) <= 12:
        return m.group(0)
    return ' '.join(x for x in (monblans_en[int(month) - 1], str(int(day)), year) if x)


def translate(text):
    """русская фраза -> английская для парсера. английский текст возвращается без изменений,
    кроме дат через точку: «12.03» — это 12 марта, а не 3 декабря"""
    s = text.lower().replace('ё', 'е')
    if not RE_CYRILLIC.search(s):
        return RE_DOTTED_DATE.sub(dotted_date, text)
    s = RE_DOTTED_TIME.sub(r'в \1:\2', s)     # «в 10.30» — это время, а не дата
    s = RE_DAY_RANGE.sub(day_range, s)          # «пн-ср», «пн-вт-ср» -> «monday thru wednesday»
    s = ' '.join(translate_word(w) for w in RE_TOKEN.findall(s))
    s = s.replace(' ,', ',')
    for regex, repl in PHRASES:
        s = regex.sub(repl, s)
    words = []
    for w in s.split():
        w2 = WORDS.get(w.strip(','), w)
        if w.endswith(',') and not w2.endswith(','):
            w2 += ','
        if RE_CYRILLIC.search(w2):
            continue            # незнакомое русское слово («встреча», «в», «по») — выбрасываем
        words.append(w2)
    s = ' '.join(words)
    # парсер теряет время, если оно стоит после «until / from / starting»:
    # «every wednesday until may 5 at 15:00» -> «every wednesday at 15:00 until may 5»
    s = RE_TIME_AFTER_END.sub(r'\1\3\2\4', s)
    return s