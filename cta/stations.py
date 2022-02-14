import pandas as pd

from typing import Optional

from pathlib import Path

from cta.route import Route


class WrongFileTypeError(Exception):
    pass


class Stations:
    """Station information for the CTA stations and stops."""

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

    def save(self, file: Optional[Path] = None) -> None:
        """Helper function to save the stations locally.

        Args:
            file: optional destination location.

        """
        if not file:
            file = Path.cwd() / "stations.csv"

        if file.suffix != ".csv":
            msg = "The file must be a csv."
            raise WrongFileTypeError(msg)

        print(f"Saving station info to {file}.")
        self.data[self.columns].to_csv(file, index=False)

    def lookup(self, name: str, route: Route) -> pd.DataFrame:
        """Helper function to search for stations ids.

        Args:
            name: name of stations to lookup.
            route: the specific train line.

        Returns:
            dataframe of the station information.

        """
        idx = self.data["station_name"].str.lower().str.contains(name.lower())
        idx = idx & self.data[route.value]

        return self.data.loc[idx, self.columns].reset_index(drop=True)


if __name__ == "__main__":
    stations = Stations()

    response = stations.lookup("Logan", route=Route.BLUE)

    stations.save()
