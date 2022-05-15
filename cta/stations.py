import pandas as pd

from typing import Optional

from pathlib import Path

from cta.route import Route


class WrongFileTypeError(Exception):
    pass


class Stations:
    """Station information for the CTA stations and stops.

    Data source found in the API documentation.

    """

    url: str = "https://data.cityofchicago.org/resource/8pix-ypme.json"

    def __init__(self):
        self.data = pd.read_json(self.url)

    @property
    def columns(self) -> list:
        """Useful columns for stations."""
        return [
            "stop_id",
            "direction_id",
            "stop_name",
            "station_name",
            "station_descriptive_name",
            "map_id",
        ]

    def lookup(self, name: str, route: Optional[Route] = None) -> pd.DataFrame:
        """Helper function to search for stations ids.

        Args:
            name: name of stations to lookup.
            route: the specific train line.

        Returns:
            dataframe of the station information.

        """
        idx = self.data["station_name"].str.lower().str.contains(name.lower())
        if route is not None:
            idx = idx & self.data[route.value]

        return self.data.loc[idx, self.columns].reset_index(drop=True)
