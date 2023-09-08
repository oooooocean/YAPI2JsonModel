from maps import SwiftType, find_value, ArrayDataPath, KotlinType, DartType
from collections import namedtuple
from exceptions import ParseError
from platform_ import Platform
from collections.abc import Coroutine

ParseAttrResult = namedtuple('ParseAttrResult', ['name', 'type', 'description', 'enumDescription'])
ParseObjectResult = namedtuple('ParseObjectResult', ['name', 'description', 'attrs'])


async def parse(content: Coroutine, platform: Platform) -> list[str]:
    """
    解析为Json Model
    """
    try:
        properties: dict = (await content)['data']
    except KeyError:
        raise ParseError(f'json解析失败, 过于简单不需要解析')
    else:
        if not len(properties):
            raise ParseError(f'json解析失败, 过于简单不需要解析')
        if array_item := _find_array_item(properties):
            properties = array_item
        else:
            properties = properties['properties']
        results = []
        __parse(properties, platform, results)
        return [platform.format(result) for result in results][::-1]


def _find_array_item(content: dict):
    """
    检查是否是数组类型
    """
    if 'items' not in content:
        return None
    if properties := content['items']['properties']:
        return properties
    return None


def __parse(attrs: dict, platform: Platform, collector: list[ParseObjectResult],
            class_name='JsonModel', description=None):
    """
    将字典解析为平台类型的数据
    :param attrs: 待解析的字典
    :param collector: 收集解析结果的数组
    :param class_name: 解析后类名
    :param description: 注释
    :return: None
    """

    results = []
    for key, value in attrs.items():
        name = key
        print(value)
        # Y-Api中的类型映射为平台类型
        match platform:
            case Platform.Swift:
                value_type = SwiftType[value['type']]
            case Platform.Kotlin:
                value_type = KotlinType[value['type']]
            case Platform.Flutter:
                value_type = DartType[value['type']]
        if value_type.is_array():
            if 'properties' in value['items']:  # 对象数组
                class_name = _capitalize(name)
                type_name = platform.format_array(class_name)
                __parse(value['items']['properties'], platform, collector, class_name=class_name)
            else:  # 常规类型数组
                match platform:
                    case Platform.Swift:
                        item_type = SwiftType[value["items"]["type"]]
                    case Platform.Kotlin:
                        item_type = KotlinType[value["items"]["type"]]
                    case Platform.Flutter:
                        item_type = DartType[value["items"]["type"]]
                type_name = platform.format_array(item_type.value)
        elif value_type.is_object():  # 嵌套对象类型
            type_name = _capitalize(name)
            __parse(value['properties'], platform, collector, class_name=type_name)
        else:
            type_name = value_type.value

        if description := value.get('title', None):  # 描述
            description = description.replace('\n', '')

        if description is None:
            if description := value.get('description', None):  # 描述
                description = description.replace('\n', '')

        if enum_description := value.get('enumDesc', None):
            enum_description = enum_description.replace('\n', '')
        results.append(ParseAttrResult(name, type_name, description, enum_description))
    collector.append(ParseObjectResult(class_name, description, results))


def _capitalize(value: str):
    """
    使字符串的第一个字母大写
    """
    return ''.join([value[:1].upper(), (value[1:])])
