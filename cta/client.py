import requests

import os

import warnings

from typing import Optional, Union, Any

from cta.route import Route
from cta.responses import ArrivalResponse, LocationResponse, FollowResponse


class TooManyArgsError(Exception):
    """Error when too many arguments are sent to the API"""


class ParamBuilder:
    """Helper class for building the parameters for the endpoints.

    Not to be used by itself.

    """

    def __init__(self, key: str):
        self.key = key

    def build(self, **kwargs) -> dict[str, Union[int, Route]]:
        params = {"key": self.key, "outputType": "JSON"}

        for key, value in kwargs.items():
            if isinstance(value, (tuple, list)):
                values = [self._resolve_type(el) for el in value]

                params[key] = values
            elif value is not None:
                params[key] = [self._resolve_type(value)]

        return params

    def _resolve_type(self, value: Union[int, Route]):
        if isinstance(value, Route):
            return value.value

        return value


class NoCredentialsError(KeyError):
    """No credentials provided."""


class RequiredArgMissingError(ValueError):
    """An argument is missing."""


class CTAClient:
    """Class to work with the different CTA endpoints.

    Currently supported endpoints:
    - arrivals
    - locations
    - follow

    Args:
        key: Chicago Transit Authority API key

    Attributes:
        version: Version of the api
        builder: ParamBuilder instance to format endpoint kwargs

    Examples:
        Initialize the client.

        >>> cta = CTAClient()

    """

    url: str = "http://lapi.transitchicago.com/api"

    def __init__(self, key: Optional[str] = None):
        try:
            self.key = key or os.environ["CTA_KEY"]
        except KeyError:
            msg = "Set the 'CTA_KEY' environment variable or provide key."
            raise NoCredentialsError(msg)

        self.version: int = 1
        self.max_number_params = 4

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
            mapid: One or more station ids.
            stpid: One or more stop ids.
            max: total number of responses. Default is all.
            route: Train line for the response.

        Returns:
            ArrivalResponse

        Example:
            Get all damen blue line arrivals.

            >>> # Lookup with cta.stations.Stations class
            >>> damen_blue_line_mapid = 40590
            >>> arrival_response = cta.arrivals(mapid=damen_blue_line_mapid)

        """
        if mapid is None and stpid is None:
            msg = "Both 'mapid' and 'stpid' cannot be null. Please provide one."
            raise RequiredArgMissingError(msg)

        self._check_number_args(mapid, "mapid")
        self._check_number_args(stpid, "stpid")

        if mapid is not None and stpid is not None:
            warnings.warn(
                "Both the 'mapid' and 'stpid' arguments were used. Might have unexpected behavior."
            )

        url = f"{self.base_url}/ttarrivals.aspx"

        params = self.builder.build(mapid=mapid, stpid=stpid, rt=route, max=max)

        return ArrivalResponse(data=self._send_request(url, params))

    def _check_number_args(self, arg, name: str) -> None:
        if isinstance(arg, list) and len(arg) > self.max_number_params:
            msg = f"{name!r} received {len(arg)} arguments. {self.max_number_params} is the maximum."
            raise TooManyArgsError(msg)

    def locations(self, route: Union[Route, list[Route]]) -> LocationResponse:
        """Get the location of trains for route(s).

        Args:
            route: Single or multiple cta.route.Route instances. No max on number
                of routes.

        Returns:
            LocationResponse

        """
        url = f"{self.base_url}/ttpositions.aspx"

        if not isinstance(route, Route) and not isinstance(route, list):
            raise ValueError(
                f"'route' must be either Route or list of Route not {type(route)}"
            )

        params = self.builder.build(rt=route)

        return LocationResponse(data=self._send_request(url, params))

    def follow(self, runnumber: Union[int, str]) -> FollowResponse:
        """Follow a given train by its runnumber.

        Args:
            runnumber: single runnumber. Only one runnumber is allowed.

        Returns:
            FollowResponse

        """
        url = f"{self.base_url}/ttfollow.aspx"

        if not isinstance(runnumber, (str, int)):
            msg = "Only one 'runnumber' allowed at a time."
            raise Exception(msg)

        params = self.builder.build(runnumber=runnumber)

        return FollowResponse(data=self._send_request(url, params))

    def _send_request(self, url: str, params: dict[str, Any]):
        response = requests.get(url, params=params)

        if not response.ok:
            msg = f"The response was not okay for {url!r}. Response was {response.text}"
            raise Exception(msg)

        return response.json()
