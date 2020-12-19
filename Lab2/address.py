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
from yargy.pipelines import morph_pipeline

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
    ['buildingName', 'buildingType', 'streetName']
)

Body = fact(
    'Body',
    ['bodyName', 'bodyType']
)

Structure = fact(
    'Structure',
    ['structureName', 'structureType']
)

Street = fact(
    'Street',
    ['streetName', 'streetType']
)

AddrPart = fact(
    'AddrPart',
    ['value']
)

def value(key):
    @property
    def field(self):
        return getattr(self, key)
    return field

class City(City):
    value = value('nameCity')

class Appart(Appart):
    value = value('appartName')

class Structure(Structure):
    value = value('structureName')

class Street(Street):
    value = value('streetName')

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

TYPE_CITY = dictionary({
    'город'
}).interpretation(
    City.typeCity
)

STRUCTURE_TYPE = dictionary({
    'строение',
    'ст'
}).interpretation(
    Structure.structureType
)


TYPE_APPART = dictionary({
    'квартира'
}).interpretation(
    Appart.typeAppart
)

BUILDING_TYPE = dictionary({
    'дом',
    'шоссе',
    'проспект',
    'улица'
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
    rule(VALUE, LETTER),
    rule(VALUE)
).interpretation(
    Building.buildingName
)

STREET_VALUE = dictionary({
    'комсомольский',
    'катукова',
    'доватора',
    'бехтеева',
    'артема',
    'алтуфьевское',
    'миттова',
    'школьная',
    'рабочая',
    'юнтоловский',
    'школьная',
    'меркулова'
})
COMPLEX_STREET = morph_pipeline([
    'юрия гагарина'
])

COMPLEX = morph_pipeline([
    'санкт-петербург',
    'нижний новгород',
    'н.новгород',
    'ростов-на-дону',
    'набережные челны',
    'улан-удэ',
    'нижний тагил',
    'комсомольск-на-амуре',
    'йошкар-ола',
    'старый оскол',
    'великий новгород',
    'южно-сахалинск',
    'петропавловск-камчатский',
    'каменск-уральский',
    'орехово-зуево',
    'сергиев посад',
    'новый уренгой',
    'ленинск-кузнецкий',
    'великие луки',
    'каменск-шахтинский',
    'усть-илимск',
    'усолье-сибирский',
    'кирово-чепецк',
])

NAME = dictionary({
    'санкт-петербург',
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
})

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

STRUCTURE = or_(
    rule(STRUCTURE_TYPE,  INT.interpretation(Structure.structureName))
).interpretation(
    Structure
)


CITY = or_(
    rule(NAME.interpretation(
        City.nameCity
    )),
    rule(TYPE_CITY, NAME.interpretation(
        City.nameCity
    )),
    COMPLEX.interpretation(
        City.nameCity
    )
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
    rule(BUILDING_TYPE, STREET_VALUE.interpretation(Building.streetName), BUILDING_VALUE),
    rule(STREET_VALUE.interpretation(Building.streetName), BUILDING_VALUE),
    rule(COMPLEX_STREET.interpretation(Building.streetName), BUILDING_VALUE),
).interpretation(
    Building
)

STREET = or_(
    rule(STREET_VALUE.interpretation(Street.streetName)),
    rule(COMPLEX_STREET.interpretation(Street.streetName))).interpretation(
    Street
)

ADDR_PART = or_(
    CITY,
    STREET,
    BUILDING,
    APPART,
    BODY,
    STRUCTURE,
).interpretation(
    AddrPart.value
)

parser = Parser(ADDR_PART)

test =  'улица меркулова дом 24'

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

    def test_36(self):
        testing_address = 'санкт-петербург школьная 20'
        building = None
        body = None
        structure = None
        city = None
        street = None
        for match in parser.findall(testing_address):
            city = match.fact.nameCity if hasattr(match.fact, 'nameCity') else city
            building = match.fact.buildingName if hasattr(match.fact, 'buildingName') else building
            body = match.fact.bodyName if hasattr(match.fact, 'bodyName') else body
            structure = match.fact.structureName if hasattr(match.fact, 'structureName') else structure
            street = match.fact.streetName if hasattr(match.fact, 'streetName') else street
        self.assertEqual(('санкт-петербург', None), (city, None))
        self.assertEqual(('школьная', None), (street, None))
        self.assertEqual(('20', None, None), (building, body, structure))

    def test_37(self):
        testing_address = 'санкт-петербург юрия гагарина 22 к2'
        building = None
        body = None
        structure = None
        city = None
        street = None
        for match in parser.findall(testing_address):
            city = match.fact.nameCity if hasattr(match.fact, 'nameCity') else city
            building = match.fact.buildingName if hasattr(match.fact, 'buildingName') else building
            body = match.fact.bodyName if hasattr(match.fact, 'bodyName') else body
            structure = match.fact.structureName if hasattr(match.fact, 'structureName') else structure
            street = match.fact.streetName if hasattr(match.fact, 'streetName') else street
        self.assertEqual(('санкт-петербург', None), (city, None))
        self.assertEqual(('юрия гагарина', None), (street, None))
        self.assertEqual(('22', '2', None), (building, body, structure))

    def test_38(self):
        testing_address = "санкт-петербург;юнтоловский 43 корпус 1"
        building = None
        body = None
        structure = None
        city = None
        street = None
        for match in parser.findall(testing_address):
            city = match.fact.nameCity if hasattr(match.fact, 'nameCity') else city
            building = match.fact.buildingName if hasattr(match.fact, 'buildingName') else building
            body = match.fact.bodyName if hasattr(match.fact, 'bodyName') else body
            structure = match.fact.structureName if hasattr(match.fact, 'structureName') else structure
            street = match.fact.streetName if hasattr(match.fact, 'streetName') else street
        self.assertEqual(('санкт-петербург', None),  (city, None))
        self.assertEqual(('юнтоловский', None), (street, None))
        self.assertEqual(('43', '1', None),  (building, body, structure))


    def test_39(self):
        testing_address = "санкт-петербург;юнтоловский 43 строение 1"
        building = None
        body = None
        structure = None
        city = None
        street = None
        for match in parser.findall(testing_address):
            city = match.fact.nameCity if hasattr(match.fact, 'nameCity') else city
            building = match.fact.buildingName if hasattr(match.fact, 'buildingName') else building
            body = match.fact.bodyName if hasattr(match.fact, 'bodyName') else body
            structure = match.fact.structureName if hasattr(match.fact, 'structureName') else structure
            street = match.fact.streetName if hasattr(match.fact, 'streetName') else street
        self.assertEqual(('санкт-петербург', None), (city, None))
        self.assertEqual(('юнтоловский', None), (street, None))
        self.assertEqual(('43',  None, '1'),  (building, body, structure))

    def test_40(self):
        testing_address = "юнтоловский 43 ст 1"
        building = None
        body = None
        structure = None
        city = None
        street = None
        for match in parser.findall(testing_address):
            city = match.fact.nameCity if hasattr(match.fact, 'nameCity') else city
            building = match.fact.buildingName if hasattr(match.fact, 'buildingName') else building
            body = match.fact.bodyName if hasattr(match.fact, 'bodyName') else body
            structure = match.fact.structureName if hasattr(match.fact, 'structureName') else structure
            street = match.fact.streetName if hasattr(match.fact, 'streetName') else street
        self.assertEqual(('юнтоловский', None), (street, None))
        self.assertEqual(('43',  None, '1'), (building, body, structure))

    def test_41(self):
        testing_address = 'проспект комсомольский 50'
        buildingValue = None
        buildingType = None
        for match in parser.findall(testing_address):
            buildingType = match.fact.buildingType if hasattr(match.fact, 'buildingType') else buildingType
            buildingValue = match.fact.streetName if hasattr(match.fact, 'streetName') else buildingValue
        self.assertEqual(('комсомольский', 'проспект'), (buildingValue, buildingType))

    def test_42(self):
        testing_address = 'город липецк улица катукова 36 a'
        buildingValue = None
        buildingType = None
        for match in parser.findall(testing_address):
            buildingType = match.fact.buildingType if hasattr(match.fact, 'buildingType') else buildingType
            buildingValue = match.fact.streetName if hasattr(match.fact, 'streetName') else buildingValue
        self.assertEqual(('катукова', 'улица'), (buildingValue, buildingType))


    def test_43(self):
        testing_address = 'город липецк доватора 18'
        buildingValue = None
        buildingType = None
        for match in parser.findall(testing_address):
            buildingType = match.fact.buildingType if hasattr(match.fact, 'buildingType') else buildingType
            buildingValue = match.fact.streetName if hasattr(match.fact, 'streetName') else buildingValue
        self.assertEqual(('доватора', None), (buildingValue, buildingType))

    def test_44(self):
        testing_address = 'ну бехтеева 9 квартира 310'
        buildingValue = None
        buildingType = None
        for match in parser.findall(testing_address):
            buildingType = match.fact.buildingType if hasattr(match.fact, 'buildingType') else buildingType
            buildingValue = match.fact.streetName if hasattr(match.fact, 'streetName') else buildingValue
        self.assertEqual(('бехтеева', None), (buildingValue, buildingType))


if __name__ == '__main__':
    unittest.main()
