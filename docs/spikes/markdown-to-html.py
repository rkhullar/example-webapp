from argparse import ArgumentParser
from pathlib import Path

import markdown


def build_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=False)
    return parser


def read_text(path: Path | str) -> str:
    with Path(path).open('r') as f:
        return f.read()


def write_text(path: Path | str, data: str):
    with Path(path).open('w') as f:
        f.write(data)


def markdown_to_html(data: str):
    return markdown.markdown(data)


if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()
    source_data = read_text(args.input)
    target_data = markdown_to_html(source_data)
    if target_path := args.output:
        write_text(target_path, target_data)
    else:
        print(target_data)
