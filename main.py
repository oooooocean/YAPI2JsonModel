import argparse
from reptile import fetch
from parse import parse, ParseError
from output import output_to_console, output_to_file

parser = argparse.ArgumentParser(description='Y-API 2 JSON BEAN🚀🚀🚀')
parser.add_argument('ids', help='需要转换的Y-api的接口id, 可多传', nargs='+')
parser.add_argument('-i', '--ios', help='生成iOS平台 Swift Decodable Model', action='store_true')
parser.add_argument('-a', '--android', help='生成Android平台 Kotlin Json Bean', action='store_true')
parser.add_argument('--file', help='将结果保存到文件中', action='store_true')

if __name__ == '__main__':
    print('🚀START')
    args = parser.parse_args()
    ids: list = args.ids
    results = []
    for api_id in args.ids:
        try:
            api_result = parse(fetch(api_id))
        except ParseError as e:
            print(f'😈{e}')
        else:
            results += api_result
    if args.file:
        output_to_file(results)
    else:
        output_to_console(results)
    print('🎆END')

