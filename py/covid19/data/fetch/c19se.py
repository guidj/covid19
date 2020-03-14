import datetime
from typing import Optional, List

import scrapy

SETTINGS = {"USER_AGENT": "BenignHoneyBadger"}


class InfectionLog(scrapy.Item):
    date = scrapy.Field()
    location = scrapy.Field()
    count = scrapy.Field()


class C19Spider(scrapy.Spider):
    name = "c19.se - data"
    start_urls = [
        "https://c19.se",
    ]

    def parse(self, response):
        for li in response.xpath("//ol/li"):
            source = strip_message(li.xpath("div/a/text()").get())
            description = strip_message(li.xpath("div/text()").get())
            count = li.xpath("span/text()").get()
            yield parse_info(source, desc=description, count=count)


def parse_info(source: Optional[str], desc: str, count: str):
    """
    If source is undefined:
        None 2020-03-09 10:47 - En person i Värmland 1
    If source is defined
        source: Person i Skåne som varit i norra Italien., desc: 2020-03-03 00:00 - , count: 1
    """
    if source:
        location = parse_location_from_message(source)
    else:
        location = parse_location_from_message(desc)

    date = parse_date_from_message(desc)

    return InfectionLog(location=location, date=date, count=int(count))


def parse_location_from_message(message: str) -> Optional[str]:
    def maybe_parse_multi_part_name(tokens: List[str]) -> str:
        def fn(items: List[str], parts: List[str]) -> str:
            if not items:
                return " ".join(parts)
            elif items[0][0].isupper():
                parts.append(items[0])
                return fn(items[1:], parts)
            else:
                return " ".join(parts)

        return fn(tokens, [])

    def fn(tokens: List[str]):
        if not tokens:
            return None
        if tokens[0] in ("i", "från") and len(tokens) > 0:
            if (
                tokens[1] in ("region", "Region")
                and len(tokens) > 1
                and tokens[2][0].isupper()
            ):
                return maybe_parse_multi_part_name(tokens[2:])
            elif tokens[1][0].isupper():
                return maybe_parse_multi_part_name(tokens[1:])
        return fn(tokens[1:])

    return fn(message.split(" "))


def parse_date_from_message(message: str) -> Optional[datetime.date]:
    tokens = message.split(" ")
    try:
        return datetime.datetime.strptime(tokens[0], "%Y-%m-%d").date()
    except ValueError:
        return None


def strip_message(msg: Optional[str]) -> Optional[str]:
    if msg:
        return msg.replace(".", " .").replace(",", " ,")
    return msg
