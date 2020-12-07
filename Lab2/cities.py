import unittest
from yargy.interpretation import fact
from yargy.predicates import (
    dictionary
)
from yargy import (
    Parser,
    rule,
    or_
)

City = fact(
    'City',
    ['name', 'type']
)
default = City(name=None, type=None)


TYPE = dictionary({
    'город'
}).interpretation(
    City.type
)

NAME = dictionary({
    'москва',
    'тольятти',
    'барнаул',
    'ижевск',
    'ульяновск',
    'владивосток',
    'ярославль',
    'чайковский',
    'азов',
    'бузулук',
    'озёрск',
    'балашов',
    'юрга',
    'кропоткин',
    'клин',
    'нальчик',
    'сургут',
    'липецк',
    'кстово'
}).interpretation(
    City.name
)

CITY = or_(
    rule(NAME),
    rule(TYPE, NAME),
).interpretation(
    City
)

parser = Parser(CITY)

class TestCity(unittest.TestCase):
    def test_1(self):
        testing_address = 'проспект комсомольский 50'
        match = default if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.name, match.type)
        self.assertEqual(res, (None, None))

    def test_2(self):
        testing_address = 'город липецк улица катукова 36 a'
        match = default if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.name, match.type)
        self.assertEqual(res, ('липецк', 'город'))

#
    def test_3(self):
        testing_address = 'сургут улица рабочая дом 31а'
        match = default if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.name, match.type)
        self.assertEqual(res, ('сургут', None))

    def test_4(self):
        testing_address = 'город липецк доватора 18'
        match = default if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.name, match.type)
        self.assertEqual(res, ('липецк', 'город'))

    def test_5(self):
        testing_address = 'ну бехтеева 9 квартира 310'
        match = default if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.name, match.type)
        self.assertEqual(res, (None, None))

    def test_6(self):
        testing_address = 'сургут югорская 30/2'
        match = default if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.name, match.type)
        self.assertEqual(res, ('сургут', None))

    def test_7(self):
        testing_address = 'индекс 12 мне вот этого не надо'
        match = default if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.name, match.type)
        self.assertEqual(res, (None, None))

    def test_8(self):
        testing_address = 'ты сургут улица 30 лет победы'
        match = default if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.name, match.type)
        self.assertEqual(res, ('сургут', None))

    def test_9(self):
        testing_address = 'надо 50% город нальчик горького 1257'
        match = default if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.name, match.type)
        self.assertEqual(res, ('нальчик', 'город'))

    def test_10(self):
        testing_address = 'null'
        match = default if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.name, match.type)
        self.assertEqual(res, (None, None))

    def test_11(self):
        testing_address = '60 мегабит я'
        match = default if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.name, match.type)
        self.assertEqual(res, (None, None))

    def test_12(self):
        testing_address = 'сургут крылова 53/4'
        match = default if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.name, match.type)
        self.assertEqual(res, ('сургут', None))

    def test_13(self):
        testing_address = 'так москва хамовнический вал но я думаю что я еще обсужу со своими домашними то есть вот у нас цифровое телевидение есть но акадо вот вы не спешите я тогда вам наберу но либо в приложения'
        match = default if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.name, match.type)
        self.assertEqual(res, ('москва', None))

    def test_14(self):
        testing_address = 'мое 3 парковая'
        match = default if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.name, match.type)
        self.assertEqual(res, (None, None))

    def test_15(self):
        testing_address = 'Пришвина 17'
        match = default if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.name, match.type)
        self.assertEqual(res, (None, None))

    def test_16(self):
        testing_address = 'Старый Гай 1 корпус 2'
        match = default if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.name, match.type)
        self.assertEqual(res, (None, None))


if __name__ == '__main__':
    unittest.main()
