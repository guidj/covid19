from typing import Dict


class Columns:
    REGION = "location"
    CONFIRMED = "confirmed"
    DEATHS = "deaths"
    RECOVERED = "recovered"
    # created
    DATE = "date"
    GROWTH_RATE = "growth_rate"

    @classmethod
    def name_mapping(cls) -> Dict[str, str]:
        return {
            "Country_Region": cls.REGION,
            "Confirmed": cls.CONFIRMED,
            "Deaths": cls.DEATHS,
            "Recovered": cls.RECOVERED,
        }

    @classmethod
    def type_mapping(cls) -> Dict[str, str]:
        return {
            cls.REGION: "category",
            cls.CONFIRMED: "int64",
            cls.DEATHS: "int64",
            cls.RECOVERED: "int64",
            cls.DATE: "datetime64",
        }
