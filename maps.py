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

    def is_array(self) -> boolean:
        return self is SwiftType.array

    def is_object(self) -> boolean:
        return self is SwiftType.object


class KotlinType(Enum):
    integer = 'Long'
    string = 'String'
    object = 'Any'
    array = 'Array'
    boolean = 'Boolean'
    number = 'Double'

    def is_array(self) -> boolean:
        return self == KotlinType.array

    def is_object(self) -> boolean:
        return self is KotlinType.object


class DartType(Enum):
    integer = 'int'
    string = 'String'
    object = 'dynamic'
    array = 'List'
    boolean = 'bool'
    number = 'double'

    def is_array(self) -> boolean:
        return self is DartType.array

    def is_object(self) -> boolean:
        return self is DartType.object


JsonBagStruct = namedtuple('JsonBagStruct', ('code', 'msg', 'data'))

JsonPath = JsonBagStruct(code=('code', 'success', 'errcode'), msg=('msg', 'errmsg'), data=('data',))

ArrayDataPath = ('data',)


def find_value(content: dict, keys: Iterable):
    for key in keys:
        if value := content.get(key, None):
            return value
    return None
