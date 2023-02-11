from enum import Enum


class Platform(Enum):
    Swift = 'swift'
    Kotlin = 'kotlin'

    def format_array(self, class_name: str):
        return f'[{class_name}]' if self is Platform.Swift else f'Array<{class_name}>'

    def format(self, value, use_class=False) -> str:
        return _format_for_swift(value, use_class) if self is Platform.Swift else _format_for_kotlin(value, use_class)


def _format_for_kotlin(value, use_class=False) -> str:
    """
    Kotlin 中Model
    """
    pass


def _format_for_swift(value, use_class=False) -> str:
    """
    Swift 中Model
    """
    classname = f'{"class" if use_class else "struct"} {value.name}: Decodable'
    attrs: list = value.attrs
    content = '\n'.join(
        [f'{_format_annotation_for_swift(item.description, item.enumDescription)}\tlet {item.name}: {item.type}'
         for item in attrs]
    )

    return '%s {\n%s\n}' % (classname, content)


def _format_annotation_for_swift(description, enum_description) -> str:
    """
    Swift 中的注释
    """
    result = ''
    if description:
        result += f'\t/// {description}\n'
    if enum_description:
        result += f'\t/// {enum_description}\n'
    return result
