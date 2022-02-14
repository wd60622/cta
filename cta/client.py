import requests

import os

import warnings

from typing import Optional, Union

from cta.route import Route
from cta.responses import ArrivalResponse, LocationResponse, FollowResponse


class TooManyArgsError(Exception):
    """Error when too many arguments are sent to the API"""


class ParamBuilder:
    """Helper class for building the parameters for the endpoints."""

    def __init__(self, key):
        self.key = key

    def build(self, **kwargs):
        params = {"key": self.key, "outputType": "JSON"}

        for key, value in kwargs.items():
            if isinstance(value, (tuple, list)):
                values = [self._resolve_type(el) for el in value]
                if len(values) > 4:
                    msg = f"{key!r} received {len(values)} arguments. 4 is the maximum."
                    raise TooManyArgsError(msg)

                params[key] = values
            elif value is not None:
                params[key] = self._resolve_type(value)

        return params

    def _resolve_type(self, value):
        if isinstance(value, Route):
            return value.value

        return value


class NoCredentialsError(KeyError):
    """No credentials provided."""


class CTAClient:
    """Class to work with the different CTA endpoints.

    Currently supported endpoints:
    - arrivals
    - locations
    - follow

    Example:
        Initialize the client.

        cta = CTAClient()

    """

    url: str = "http://lapi.transitchicago.com/api"

    def __init__(self, key: Optional[str] = None):
        try:
            self.key = key or os.environ["CTA_KEY"]
        except KeyError:
            msg = "Set the 'CTA_KEY' environment variable or provide key."
            raise NoCredentialsError(msg)

        self.version: int = 1

        self.builder = ParamBuilder(key=self.key)

    @property
    def base_url(self) -> str:
        return f"{self.url}/{self.version:.1f}"

    def arrivals(
        self,
        mapid: Optional[Union[int, list[int]]] = None,
        stpid: Optional[Union[int, list[int]]] = None,
        max: Optional[int] = None,
        route: Optional[Route] = None,
    ) -> ArrivalResponse:
        """Get the arrivals for station(s), stop(s), and route(s).

        Args:
            mapid:
            stpid:
            max:
            route:

        Returns:


        """
        if mapid is None and stpid is None:
            msg = "Both 'mapid' and 'stpid' cannot be null. Please provide one."
            raise Exception(msg)

        if mapid is not None and stpid is not None:
            warnings.warn(
                "Both the 'mapid' and 'stpid' arguments were used. Might have unexpected behavior."
            )

        url = f"{self.base_url}/ttarrivals.aspx"

        params = self.builder.build(mapid=mapid, stpid=stpid, rt=route, max=max)

        return ArrivalResponse(data=self._send_request(url, params))

    def locations(self, route: Union[Route, list[Route]]) -> LocationResponse:
        """Get the location of"""
        url = f"{self.base_url}/ttpositions.aspx"

        params = self.builder.build(rt=route)

        return LocationResponse(data=self._send_request(url, params))

    def follow(self, runnumber: str) -> FollowResponse:
        url = f"{self.base_url}/ttfollow.aspx"

        if not isinstance(runnumber, (str, int)):
            msg = "Only one 'runnumber' allowed at a time."
            raise Exception(msg)

        params = self.builder.build(runnumber=runnumber)

        return FollowResponse(data=self._send_request(url, params))

    def _send_request(self, url, params):
        response = requests.get(url, params=params)

        if not response.ok:
            msg = f"The response was not okay for {url!r}."
            raise Exception(msg)

        return response.json()


if __name__ == "__main__":
    cta = CTAClient()

    damen_mapid = 40590
    logan_mapid = 41020
    mapids = [40540, 40900, 40080, 40380]
    # mapids = [40830, 41270]
    stpids = [30162, 30161, 30022, 30023]

    # response = cta.arrivals(mapid=mapids, stpid=stpids, route=Route.BLUE)
    response = cta.locations(route=Route.BLUE)

    # response = cta.follow(runnumber=426)

    from rich import print_json

    # response = cta.locations(Route.BLUE, Route.RED)
