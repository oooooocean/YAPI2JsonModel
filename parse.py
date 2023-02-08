from json import loads
from maps import SwiftType, find_value, ArrayDataPath
from collections import namedtuple
from exceptions import ParseError

ParseAttrResult = namedtuple('ParseAttrResult', ['name', 'type', 'description', 'enumDescription'])
ParseObjectResult = namedtuple('ParseObjectResult', ['name', 'description', 'attrs'])


def parse(content: dict) -> list[str]:
    try:
        properties: dict = content['data']['properties']
    except KeyError:
        raise ParseError(f'json解析失败, 过于简单不需要解析')
    if not len(properties):
        raise ParseError(f'json解析失败, 过于简单不需要解析')
    if array_item := _find_array_item(properties):
        properties = array_item
    results = []
    __parse(properties, results)
    return [_format_for_swift(result) for result in results][::-1]


def _find_array_item(content: dict):
    if 'total' not in content:
        return None
    if properties := find_value(content, ArrayDataPath)['items']['properties']:
        return properties
    return None


def __parse(attrs: dict, collector: list[ParseObjectResult], class_name='JsonModel', description=None):
    results = []
    for key, value in attrs.items():
        name = key
        # 类型
        value_type = SwiftType[value['type']]
        if value_type is SwiftType.array:
            if 'properties' in value['items']:  # 对象数组
                class_name = _capitalize(name)
                type_name = f'[{class_name}]'
                __parse(value['items']['properties'], collector, class_name=class_name)
            else:  # 常规类型数组
                type_name = f'[{SwiftType[value["items"]["type"]].value}]'
        elif value_type is SwiftType.object:  # 嵌套对象类型
            type_name = _capitalize(name)
            __parse(value['properties'], collector, class_name=type_name)
        else:
            type_name = value_type.value
        # 描述
        if description := value.get('description', None):
            description = description.replace('\n', '')
        if enum_description := value.get('enumDesc', None):
            enum_description = enum_description.replace('\n', '')
        results.append(ParseAttrResult(name, type_name, description, enum_description))
    collector.append(ParseObjectResult(class_name, description, results))


def _format_annotation_for_swift(description, enum_description) -> str:
    result = ''
    if description:
        result += f'\t/// {description}\n'
    if enum_description:
        result += f'\t/// {enum_description}\n'
    return result


def _format_for_swift(value: ParseObjectResult, use_class=False) -> str:
    classname = f'{"class" if use_class else "struct"} {value.name}: Decodable'
    attrs: list[ParseAttrResult] = value.attrs
    content = '\n'.join(
        [f'{_format_annotation_for_swift(item.description, item.enumDescription)}\tlet {item.name}: {item.type}'
         for item in attrs]
    )

    return '%s {\n%s\n}' % (classname, content)


def _capitalize(value: str):
    return ''.join([value[:1].upper(), (value[1:])])
