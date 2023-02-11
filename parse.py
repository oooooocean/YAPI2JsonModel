from maps import SwiftType, find_value, ArrayDataPath, KotlinType
from collections import namedtuple
from exceptions import ParseError
from platform import Platform

ParseAttrResult = namedtuple('ParseAttrResult', ['name', 'type', 'description', 'enumDescription'])
ParseObjectResult = namedtuple('ParseObjectResult', ['name', 'description', 'attrs'])


def parse(content: dict, platform: Platform) -> list[str]:
    """
    解析为Json Model
    """
    try:
        properties: dict = content['data']['properties']
    except KeyError:
        raise ParseError(f'json解析失败, 过于简单不需要解析')
    else:
        if not len(properties):
            raise ParseError(f'json解析失败, 过于简单不需要解析')
        if array_item := _find_array_item(properties):
            properties = array_item
        results = []
        __parse(properties, results)
        return [platform.format(result) for result in results][::-1]


def _find_array_item(content: dict):
    """
    检查是否是数组类型
    """
    if 'total' not in content:
        return None
    if properties := find_value(content, ArrayDataPath)['items']['properties']:
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
        value_type = SwiftType[value['type']] if platform is Platform.Swift else KotlinType[value['type']]  # Y-Api中的类型映射为平台类型
        if value_type.is_array():
            if 'properties' in value['items']:  # 对象数组
                class_name = _capitalize(name)
                type_name = platform.format_array(class_name)
                __parse(value['items']['properties'], collector, class_name=class_name)
            else:  # 常规类型数组
                item_type = SwiftType[value["items"]["type"]] if platform is Platform.Swift else KotlinType[value["items"]["type"]]
                type_name = platform.format_array(item_type.value())
        elif value_type.is_object():  # 嵌套对象类型
            type_name = _capitalize(name)
            __parse(value['properties'], collector, class_name=type_name)
        else:
            type_name = value_type.value
        if description := value.get('description', None): # 描述
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
