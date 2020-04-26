"""
Module for post processing files for website
Generates partials with visualizations.
"""
import argparse
import html.parser
import os
import os.path
from typing import List

import scrapy


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--plots-path", required=True, help="Dir with global and region plots"
    )
    arg_parser.add_argument("--files", nargs="+", required=True, help="Files to parse")
    arg_parser.add_argument(
        "--output-path", required=True, help="Path to output partials"
    )
    return arg_parser.parse_args()


def remove_tags(content: str, tag: str) -> str:
    return content.lstrip("<{}>".format(tag)).rstrip("</{}>".format(tag)).strip()


def generate_partials(plots_path: str, files: List[str], output_path: str) -> None:
    for file_name in files:
        file_path = os.path.join(plots_path, file_name)
        _, extension = os.path.splitext(file_path)
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
