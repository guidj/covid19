"""
Module for post processing files for website
Generates partials with visualizations.
"""
import argparse
import os
import os.path
from typing import List, Sequence
import dataclasses

import scrapy
import scrapy.http


@dataclasses.dataclass(frozen=True)
class Args:
    plots_path: str
    files: Sequence[str]
    output_path: str


def parse_args() -> Args:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--plots-path", required=True, help="Dir with global and region plots"
    )
    arg_parser.add_argument("--files", nargs="+", required=True, help="Files to parse")
    arg_parser.add_argument(
        "--output-path", required=True, help="Path to output partials"
    )
    kwargs, _ = arg_parser.parse_known_args()
    return Args(**vars(kwargs))


def remove_tags(content: str, tag: str) -> str:
    return content.lstrip(f"<{tag}>").rstrip(f"</{tag}>").strip()


def generate_partials(plots_path: str, files: List[str], output_path: str) -> None:
    for file_name in files:
        file_path = os.path.join(plots_path, file_name)
        output_file_name = os.path.join(output_path, file_name)

        with open(file_path) as file:
            response = scrapy.http.HtmlResponse(
                url=file_path, body=file.read().encode("UTF-8")
            )
            body = remove_tags(response.selector.xpath("//body").get(), "body")

        with open(output_file_name, "w") as file:
            file.write(body)


def main(plots_path: str, files: List[str], output_path: str) -> None:
    generate_partials(plots_path, files, output_path)


if __name__ == "__main__":
    args = parse_args()
    main(args.plots_path, args.files, args.output_path)
