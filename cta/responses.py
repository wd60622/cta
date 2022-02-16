import pandas as pd

from abc import ABC, abstractmethod


class Trains:
    """Class to process train level data."""

    def __init__(self, data: list[dict]):
        self.data = data

    def to_frame(self):
        df_trains = pd.DataFrame.from_records(self.data)

        for col in ["prdt", "arrT"]:
            df_trains[col] = pd.to_datetime(df_trains[col])

        now = pd.Timestamp("now")
        df_trains["time_til_arrival"] = (
            df_trains["arrT"] - now
        ).dt.total_seconds() / 60

        df_trains["time_since_prediction"] = (
            now - df_trains["prdt"]
        ).dt.total_seconds() / 60

        return df_trains


class Response(ABC):
    """Abstract class for a response for the CTA endpoints."""

    def __init__(self, data: dict):
        self.data = data

        self._check_input()

    def _check_input(self):
        body = self.data["ctatt"]
        if int(body["errCd"]) >= 100:
            msg = f"Recieved code {body['errCd']} with message: {body['errNm']!r}"
            raise ValueError(msg)

    @abstractmethod
    def to_frame(self) -> pd.DataFrame:
        """Translate the response into DataFrame object."""


class ETAResponse(Response):
    """Common functionality between endpoint data."""

    def to_frame(self) -> pd.DataFrame:
        payload = self.data["ctatt"]
        if "eta" not in payload:
            return pd.DataFrame()

        return Trains(payload["eta"]).to_frame()


class ArrivalResponse(ETAResponse):
    """Response from arrivals endpoint."""


class FollowResponse(ETAResponse):
    """Response from follow endpoint."""


class LocationResponse(Response):
    """Response from location endpoint."""

    def to_frame(self) -> pd.DataFrame:
        dfs = [
            Trains(data=route["train"]).to_frame().assign(train=route["@name"])
            for route in self.data["ctatt"]["route"]
        ]

        return pd.concat(dfs, ignore_index=True)
