import unittest
from yargy.interpretation import fact
from yargy.predicates import (
    dictionary,
    type,
    in_caseless,
    in_
)
from yargy import (
    Parser,
    rule,
    or_,
)

City = fact(
    'City',
    ['nameCity', 'typeCity']
)

Appart = fact(
    'Appart',
    ['appartName', 'typeAppart']
)

Building = fact(
    'Building',
    ['buildingName', 'buildingType']
)

Body = fact(
    'Body',
    ['bodyName', 'bodyType']
)

AddrPart = fact(
    'AddrPart',
    ['value']
)

defaultCity = City(nameCity=None)

defaultAppart = Appart(appartName=None, typeAppart=None)

def value(key):
    @property
    def field(self):
        return getattr(self, key)
    return field

class City(City):
    value = value('nameCity')

class Appart(Appart):
        value = value('appartName')

class Building(Building):
        value = value('buildingName')

class AddrPart(AddrPart):
    @property
    def obj(self):
        from natasha import obj

        part = self.value
        return obj.AddrPart(part.value, part.type)

INT = type('INT')

LETTER = in_caseless(set('абвгдежзиклмнопрстуфхшщэюя'))

TYPE = dictionary({
    'город'
}).interpretation(
    City.typeCity
)

TYPE_APPART = dictionary({
    'квартира'
}).interpretation(
    Appart.typeAppart
)

BUILDING_TYPE = dictionary({
    'дом',
    'шоссе',
    'проспект'
}
).interpretation(
    Building.buildingType
)

VALUE = rule(
    INT,
    LETTER.optional()
)

SEP = in_(r'/\-')

BUILDING_VALUE = or_(
    rule(VALUE),
    rule(VALUE, VALUE),
    rule(VALUE, LETTER),
).interpretation(
    Building.buildingName
)

STREET = dictionary({
    'комсомольский',
    'катукова',
    'доватора',
    'бехтеева',
    'артема',
    'алтуфьевское',
    'миттова',
    'школьная',
    'юрия гагарина',
    'гагарина',
    'юнтоловский'
})

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
    City.nameCity
)

BODY_TYPE = dictionary({
    'корпус',
    'к'
}
).interpretation(
    Body.bodyType
)

BODY = or_(
    rule(BODY_TYPE, INT.interpretation(Body.bodyName))
).interpretation(
    Body
)


CITY = or_(
    rule(NAME),
    rule(TYPE, NAME)
).interpretation(
    City
)

APPART = or_(
    rule(TYPE_APPART, INT.interpretation(Appart.appartName))
).interpretation(
    Appart
)

BUILDING = or_(
    rule(BUILDING_TYPE, BUILDING_VALUE),
    rule(STREET, BUILDING_VALUE)
).interpretation(
    Building
)

ADDR_PART = or_(
    BUILDING,
    CITY,
    APPART,
    BODY
).interpretation(
    AddrPart.value
)

parser = Parser(ADDR_PART)

test = 'питер гагарина 22 к2'

# print(parser.findall(test))
for matc in parser.findall(test):
    print(matc.fact)


class TestCity(unittest.TestCase):
    def test_1(self):
        testing_address = 'проспект комсомольский 50'
        match = (None, None) if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.nameCity if hasattr(match, 'nameCity') else None, match.typeCity if hasattr(match, 'typeCity') else None)
        self.assertEqual(res, (None, None))

    def test_2(self):
        testing_address = 'город липецк улица катукова 36 a'
        match = (None, None)  if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.nameCity if hasattr(match, 'nameCity') else None, match.typeCity if hasattr(match, 'typeCity') else None)
        self.assertEqual(res, ('липецк', 'город'))

#
    def test_3(self):
        testing_address = 'сургут улица рабочая дом 31а'
        match = (None, None)  if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.nameCity if hasattr(match, 'nameCity') else None, match.typeCity if hasattr(match, 'typeCity') else None)
        self.assertEqual(res, ('сургут', None))

    def test_4(self):
        testing_address = 'город липецк доватора 18'
        match = (None, None)  if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.nameCity if hasattr(match, 'nameCity') else None, match.typeCity if hasattr(match, 'typeCity') else None)
        self.assertEqual(res, ('липецк', 'город'))

    def test_5(self):
        testing_address = 'ну бехтеева 9 квартира 310'
        match = (None, None)  if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.nameCity if hasattr(match, 'nameCity') else None, match.typeCity if hasattr(match, 'typeCity') else None)
        self.assertEqual(res, (None, None))

    def test_6(self):
        testing_address = 'сургут югорская 30/2'
        match = (None, None)  if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.nameCity if hasattr(match, 'nameCity') else None, match.typeCity if hasattr(match, 'typeCity') else None)
        self.assertEqual(res, ('сургут', None))

    def test_7(self):
        testing_address = 'индекс 12 мне вот этого не надо'
        match = (None, None)  if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.nameCity if hasattr(match, 'nameCity') else None, match.typeCity if hasattr(match, 'typeCity') else None)
        self.assertEqual(res, (None, None))

    def test_8(self):
        testing_address = 'ты сургут улица 30 лет победы'
        match = (None, None)  if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.nameCity if hasattr(match, 'nameCity') else None, match.typeCity if hasattr(match, 'typeCity') else None)
        self.assertEqual(res, ('сургут', None))

    def test_9(self):
        testing_address = 'надо 50% город нальчик горького 1257'
        match = (None, None)  if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.nameCity if hasattr(match, 'nameCity') else None, match.typeCity if hasattr(match, 'typeCity') else None)
        self.assertEqual(res, ('нальчик', 'город'))

    def test_10(self):
        testing_address = 'null'
        match = (None, None)  if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.nameCity if hasattr(match, 'nameCity') else None, match.typeCity if hasattr(match, 'typeCity') else None)
        self.assertEqual(res, (None, None))

    def test_11(self):
        testing_address = '60 мегабит я'
        match = (None, None)  if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.nameCity if hasattr(match, 'nameCity') else None, match.typeCity if hasattr(match, 'typeCity') else None)
        self.assertEqual(res, (None, None))

    def test_12(self):
        testing_address = 'сургут крылова 53/4'
        match = (None, None)  if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.nameCity if hasattr(match, 'nameCity') else None, match.typeCity if hasattr(match, 'typeCity') else None)
        self.assertEqual(res, ('сургут', None))

    def test_13(self):
        testing_address = 'так москва хамовнический вал но я думаю что я еще обсужу со своими домашними то есть вот у нас цифровое телевидение есть но акадо вот вы не спешите я тогда вам наберу но либо в приложения'
        match = (None, None)  if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.nameCity if hasattr(match, 'nameCity') else None, match.typeCity if hasattr(match, 'typeCity') else None)
        self.assertEqual(res, ('москва', None))

    def test_14(self):
        testing_address = 'мое 3 парковая'
        match = (None, None)  if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.nameCity if hasattr(match, 'nameCity') else None, match.typeCity if hasattr(match, 'typeCity') else None)
        self.assertEqual(res, (None, None))

    def test_15(self):
        testing_address = 'Пришвина 17'
        match = (None, None)  if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.nameCity if hasattr(match, 'nameCity') else None, match.typeCity if hasattr(match, 'typeCity') else None)
        self.assertEqual(res, (None, None))

    def test_16(self):
        testing_address = 'Старый Гай 1 корпус 2'
        match = (None, None) if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.nameCity if hasattr(match, 'nameCity') else None, match.typeCity if hasattr(match, 'typeCity') else None)
        self.assertEqual(res, (None, None))

    def test_17(self):
        testing_address = 'проспект комсомольский 50'
        match = None if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = match.appartName if hasattr(match, 'appartName') else None
        self.assertEqual(res, None)

    def test_18(self):
        testing_address = 'город липецк улица катукова 36 a'
        match = None if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = match.appartName if hasattr(match, 'appartName') else None
        self.assertEqual(res, None)

    def test_19(self):
        testing_address = 'сургут улица рабочая дом 31а'
        match = None if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = match.appartName if hasattr(match, 'appartName') else None
        self.assertEqual(res, None)

    def test_20(self):
        testing_address = 'город липецк доватора 18'
        match = None if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = match.appartName if hasattr(match, 'appartName') else None
        self.assertEqual(res, None)

    def test_21(self):
        testing_address = 'ну бехтеева 9 квартира 310'
        res = None
        for match in parser.findall(testing_address):
            res = match.fact.appartName if hasattr(match.fact, 'appartName') else res
        self.assertEqual(res, '310')

    def test_22(self):
        testing_address = 'Кусковская 19 корпус 1'
        match = None if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = match.appartName if hasattr(match, 'appartName') else None
        self.assertEqual(res, None)

    def test_23(self):
        testing_address = 'марша захарова 12 маршала захарова дом 12'
        match = None if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = match.appartName if hasattr(match, 'appartName') else None
        self.assertEqual(res, None)

    def test_24(self):
        testing_address = 'null'
        match = None if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = match.appartName if hasattr(match, 'appartName') else None
        self.assertEqual(res, None)

    def test_25(self):
        testing_address = 'проспект комсомольский 50'
        match = None if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.buildingName if hasattr(match, 'buildingName') else None, match.bodyName if hasattr(match, 'bodyName') else None, None)
        self.assertEqual(res, ('50', None, None))

    def test_26(self):
        testing_address = 'город липецк улица катукова 36 a'
        match = None if parser.find(testing_address) is None else parser.find(testing_address).fact
        res = (match.buildingName if hasattr(match, 'buildingName') else None, match.bodyName if hasattr(match, 'bodyName') else None, None)
        self.assertEqual(res, ('36 a', None, None))

    def test_27(self):
        testing_address = 'сургут улица рабочая дом 31а'
        building = None
        body = None
        for match in parser.findall(testing_address):
            building = match.fact.buildingName if hasattr(match.fact, 'buildingName') else building
            body = match.fact.bodyName if hasattr(match.fact, 'bodyName') else body
        self.assertEqual((building, body,None), ('31а', None, None))

    def test_28(self):
        testing_address = 'город липецк доватора 18'
        building = None
        body = None
        for match in parser.findall(testing_address):
            building = match.fact.buildingName if hasattr(match.fact, 'buildingName') else building
            body = match.fact.bodyName if hasattr(match.fact, 'bodyName') else body
        self.assertEqual((building, body, None), ('18', None, None))

    def test_29(self):
        testing_address = 'ну бехтеева 9 квартира 310'
        building = None
        body = None
        for match in parser.findall(testing_address):
            building = match.fact.buildingName if hasattr(match.fact, 'buildingName') else building
            body = match.fact.bodyName if hasattr(match.fact, 'bodyName') else body
        self.assertEqual((building, body, None), ('9', None, None))

    def test_30(self):
        testing_address = 'артема 32 квартира 8'
        building = None
        body = None
        for match in parser.findall(testing_address):
            building = match.fact.buildingName if hasattr(match.fact, 'buildingName') else building
            body = match.fact.bodyName if hasattr(match.fact, 'bodyName') else body
        self.assertEqual((building, body, None), ('32', None, None))

    def test_31(self):
        testing_address = 'город липецк полиграфическая дом 4'
        building = None
        body = None
        for match in parser.findall(testing_address):
            building = match.fact.buildingName if hasattr(match.fact, 'buildingName') else building
            body = match.fact.bodyName if hasattr(match.fact, 'bodyName') else body
        self.assertEqual((building, body, None), ('4', None, None))

    def test_32(self):
        testing_address = 'сколько стоит нет arkadata у нас есть москва каширское шоссе 55 корпус 1'
        building = None
        body = None
        for match in parser.findall(testing_address):
            building = match.fact.buildingName if hasattr(match.fact, 'buildingName') else building
            body = match.fact.bodyName if hasattr(match.fact, 'bodyName') else body
        self.assertEqual((building, body, None), ('55', '1', None))

    def test_33(self):
        testing_address = 'люберцы октябрьский проспект 10 корпус 1'
        building = None
        body = None
        for match in parser.findall(testing_address):
            building = match.fact.buildingName if hasattr(match.fact, 'buildingName') else building
            body = match.fact.bodyName if hasattr(match.fact, 'bodyName') else body
        self.assertEqual((building, body, None), ('10', '1', None))

    def test_34(self):
        testing_address = 'бульвар миттова 24'
        building = None
        body = None
        for match in parser.findall(testing_address):
            building = match.fact.buildingName if hasattr(match.fact, 'buildingName') else building
            body = match.fact.bodyName if hasattr(match.fact, 'bodyName') else body
        self.assertEqual((building, body, None), ('24', None, None))

    def test_35(self):
        testing_address = 'стол вы знаете москва алтуфьевское 78'
        building = None
        body = None
        for match in parser.findall(testing_address):
            building = match.fact.buildingName if hasattr(match.fact, 'buildingName') else building
            body = match.fact.bodyName if hasattr(match.fact, 'bodyName') else body
        self.assertEqual((building, body, None), ('78', None, None))


if __name__ == '__main__':
    unittest.main()
