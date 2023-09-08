from enum import Enum


class Platform(Enum):
    Swift = 'swift'
    Kotlin = 'kotlin'
    Flutter = 'flutter'

    def format_array(self, class_name: str):
        match self:
            case Platform.Swift:
                return f'[{class_name}]'
            case _:
                return f'List<{class_name}>'

    def format(self, value, use_class=False) -> str:
        match self:
            case Platform.Swift:
                return _format_for_swift(value, use_class)
            case Platform.Kotlin:
                return _format_for_kotlin(value, use_class)
            case Platform.Flutter:
                return _format_for_flutter(value)


def _format_for_kotlin(value, use_class=False) -> str:
    class_name = f'{"class" if use_class else "data class"} {value.name}'
    attrs: list = value.attrs
    content = '\n'.join(
        [
            f'{_format_annotation_for_kotlin(item.description, item.enumDescription)}\tval {item.name}: {item.type}?,'
            for item in attrs]
    )

    return '%s (\n%s\n)' % (class_name, content)


def _format_for_swift(value, use_class=False) -> str:
    """
    Swift 中Model
    """
    classname = f'{"class" if use_class else "struct"} {value.name}: Decodable'
    attrs: list = value.attrs
    content = '\n'.join(
        [
            f'{_format_annotation_for_swift_or_flutter(item.description, item.enumDescription)}\tlet {item.name}: {item.type}'
            for item in attrs]
    )

    return '%s {\n%s\n}' % (classname, content)


def _format_for_flutter(value) -> str:
    """
    Flutter 中Model
    """
    import_string = "import 'package:json_annotation/json_annotation.dart';"
    classname = f'@JsonSerializable()\nclass {value.name}'
    attrs: list = value.attrs
    content = '\n'.join(
        [
            f'{_format_annotation_for_swift_or_flutter(item.description, item.enumDescription)}\tfinal {item.type} {item.name};'
            for item in attrs]
    )
    initializer = f'\t{value.name}({", ".join([f"this.{item.name}" for item in attrs])});'
    factory = f'\tfactory {value.name}.fromJson(Map<String, dynamic> json) => _${value.name}FromJson(json);\n\n\t' \
              f'Map<String, dynamic> toJson() => _${value.name}ToJson(this);'

    return '%s\n\n%s {\n%s\n\n%s\n\n%s\n}' % (import_string, classname, content, initializer, factory)


def _format_annotation_for_swift_or_flutter(description, enum_description) -> str:
    """
    Swift 中的注释
    """
    result = ''
    if description:
        result += f'\t/// {description}\n'
    if enum_description:
        result += f'\t/// {enum_description}\n'
    return result


def _format_annotation_for_kotlin(description, enum_description) -> str:
    """
    Swift 中的注释
    """
    result = ''
    if description:
        result += f'\t// {description}\n'
    if enum_description:
        result += f'\t// {enum_description}\n'
    return result
