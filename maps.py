from enum import Enum
from collections import namedtuple
from collections.abc import Iterable


class SwiftType(Enum):
    integer = 'Int'
    string = 'String'
    object = 'Any'
    array = 'Array'
    boolean = 'Bool'
    number = 'Double'


JsonBagStruct = namedtuple('JsonBagStruct', ('code', 'msg', 'data'))

JsonPath = JsonBagStruct(code=('code', ), msg=('msg', ), data=('data', ))

ArrayDataPath = ('data', )


def find_value(content: dict, keys: Iterable):
    for key in keys:
        if value := content.get(key, None):
            return value
    return None
