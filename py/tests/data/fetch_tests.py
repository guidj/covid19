import unittest
import datetime

from covid19.data import fetch


class ParseLocationFromMessageTest(unittest.TestCase):
    def test_parse_location_from_source_with_simple_case_returns_location(self):
        self.assertEqual("Stockholm", fetch.parse_location_from_message("i Stockholm"))
        self.assertEqual(
            "Jönköping", fetch.parse_location_from_message("från Jönköping")
        )

    def test_parse_location_from_source_with_region_prefix_returns_location(self):
        self.assertEqual(
            "Jämtland", fetch.parse_location_from_message("i Region Jämtland")
        )
        self.assertEqual(
            "Sörmland", fetch.parse_location_from_message("i region Sörmland")
        )

    def test_parse_location_from_source_with_multipart_name_prefix_returns_location(
        self,
    ):
        self.assertEqual(
            "Västra Götaland", fetch.parse_location_from_message("i Västra Götaland")
        )

    def test_parse_location_from_message_with_multiple_key_words_returns_location(self):
        self.assertEqual(
            "Stockholm",
            fetch.parse_location_from_message("i Stockholm i Sverige i Monad"),
        )
        self.assertEqual(
            "Monad", fetch.parse_location_from_message("i stockholm i Monad")
        )

    def test_parse_location_from_message_with_empty_string_returns_None(self):
        self.assertIsNone(fetch.parse_location_from_message(""))


class ParseDateFromMessageTest(unittest.TestCase):
    def test_parse_date_from_message_with_simple_case_returns_date(self):
        self.assertEqual(
            datetime.date(2020, 1, 1), fetch.parse_date_from_message("2020-01-01")
        )

    def test_parse_date_from_message_with_padded_data_returns_date(self):
        self.assertEqual(
            datetime.date(2020, 1, 1), fetch.parse_date_from_message("2020-01-01 12:23")
        )

    def test_parse_date_from_message_with_empty_string_returns_None(self):
        self.assertIsNone(fetch.parse_date_from_message(""))

    def test_parse_date_from_source_with_wrong_format_returns_None(self):
        self.assertIsNone(fetch.parse_date_from_message("18819191"))
