
def output_to_console(contents):
    for content in contents:
        print(content, end='\n\n')


def output_to_file(contents: list[str], filename='JsonModel'):
    content = '\n\n'.join(contents)
    with open(f'{filename}.swift', 'w') as fp:
        fp.write(content)

