import re

holis = (
    r'(понедельник)|(пн)',    
    r'вт(орник)?',
    r'ср(еда)?',
    r'(четверг)|(чт)',
    r'(пт)|(пятница)',
    r'(сб)|субб(ота)?',
    r'(вс)|воскресен(ье|ие)?',
    r'будни',
    r'выходн(ой|ые)'
)
RE_holis = [re.compile(r) for r in holis]
RE_PLURAL_DOW = re.compile('|'.join( ['понедельникам', 'вторникам', 'средам',
    'четвергам', 'пятницам', 'субботам', 'воскресеньям']))
RE_DOW = re.compile('(' + ')$|('.join(holis) + ')$')
RE_PLURAL_WEEKDAY = re.compile('будни|выходные|выходной|%s'%RE_PLURAL_DOW.pattern)
weekday_codes = [ 'пн','вт','ср','чт','пт', 'сб', 'вс', 'пн,вт,ср,чт,пт',
'сб,вс']
ordered_weekday_codes = ('', 'вс', 'пн', 'вт', 'ср', 'чт', 'пт', 'сб')
next_day = dict(MO='вт', TU='ср', WE='чт', TH='пт', FR='сб', SA='вс', SU='пн')
day_names = dict(MO='пн', TU='вт', WE='ср', TH='чт', FR='пт', SA='сб', SU='вс')
plural_day_names = dict(MO='понедельник', TU='вторник', WE='среду', TH='четверг', FR='пятницу', SA='субботу', SU='воскресенье')

monblans = (
    r'янв(арь)?',
    r'фев(р?аль)?',
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
RE_monblans = [re.compile(r + '$') for r in monblans]
RE_MOY = re.compile('(' + ')$|('.join(monblans) + ')$')
RE_MOY_NOT_ANCHORED = re.compile('(' + ')|('.join(monblans) + ')')

units = ['день', 'неделя', 'месяц', 'год', 'час', 'минута', 'мин', 'с', 'секунд'] # Issue #3
units_freq = ['ежедневно', 'еженедельно', 'ежемесячно', 'ежегодно', 'ежечасно', 'ежеминутно', 'поминутно', 'ежесекундно', 'посекундно'] # Issue #3
RE_UNITS = re.compile(r'^(' + 's?|'.join(units) + '?)$')

ordinals = (
    r'первый',
    r'второй',
    r'третий',
    r'четвертый',
    r'пятй',
    r'шестой',
    r'седьмой',
    r'восьмой',
    r'девятый',
    r'десятый',
    r'последний',        # Issue #18
    )
RE_ORDINALS = [re.compile(r + '$') for r in ordinals]
RE_ORDINAL = re.compile(r'\d+(st|nd|rd|th)$|' + '$|'.join(ordinals))
RE_ORDINAL_NOT_ANCHORED = re.compile(r'\d+(st|nd|rd|th)|' + '|'.join(ordinals))
numbers = (
    r'ноль',
    r'один',
    r'два',
    r'три',
    r'четыре',
    r'пять',
    r'шесть',
    r'семь',
    r'восемь',
    r'девять',
    r'десять',
    )
RE_NUMBERS = [re.compile(r + '$') for r in numbers]
RE_NUMBER = re.compile('(' + '|'.join(numbers) + r')$|(\d+)$')
RE_NUMBER_NOT_ANCHORED = re.compile('(' + '|'.join(numbers) + r')|(\d+)')

RE_EVERY = re.compile(r'(every|each|once)$')

RE_THROUGH = re.compile(r'(through|thru)$')

RE_DAILY = re.compile(r'daily|everyday')
RE_RECURRING_UNIT = re.compile(r'weekly|monthly|yearly')

# getters
def get_number(s):
    try:
        return int(s)
    except ValueError:
        return numbers.index(s)

def get_ordinal_index(s):
    try:
        return int(s[:-2])
    except ValueError:
        pass
    sign = -1 if s[0] == '-' else 1     # Issue #18
    for i, reg in enumerate(RE_ORDINALS):
        if reg.match(s):
            if i == 10:         # Issue #18
                return -1       # Issue #18
            return sign * (i + 1)   # Issue #18
    raise ValueError        # pragma nocover

def get_DoW(s):
    for i, dow in enumerate(RE_holis):
        if dow.search(s):
            return weekday_codes[i].split(',')
    raise ValueError        # pragma nocover

def get_MoY(s):
    for i, moy in enumerate(RE_monblans):
        if moy.search(s):
            return i + 1
    raise ValueError        # pragma nocover

def get_unit_freq(s):
    for i, unit in enumerate(units):
        if unit in s:
            return units_freq[i]
    raise ValueError        # pragma nocover

