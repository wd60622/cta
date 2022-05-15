import pytest

import pandas as pd

from cta.client import (
    ParamBuilder,
    CTAClient,
    RequiredArgMissingError,
    TooManyArgsError,
)
from cta import Route
from cta.responses import FollowResponse, ArrivalResponse, LocationResponse

from pathlib import Path
import json


TEST_DATA_DIR = Path(__file__).parent / "data"
FAKE_KEY = "abc"


@pytest.fixture
def param_builder():
    return ParamBuilder(key=FAKE_KEY)


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        (
            {
                "mapid": 1,
                "stpid": 1,
            },
            {"mapid": [1], "stpid": [1]},
        ),
        ({"mapid": [1, 2, 3]}, {"mapid": [1, 2, 3]}),
        (
            {"mapid": [1, 2, 3], "route": [Route.BLUE, Route.YELLOW]},
            {"mapid": [1, 2, 3], "route": ["blue", "y"]},
        ),
    ],
)
def test_build_params(param_builder, kwargs, expected):
    response = param_builder.build(**kwargs)
    for key, value in expected.items():
        assert response[key] == value


def load_test_data(file_name: str) -> dict:
    file = TEST_DATA_DIR / file_name
    if not file.exists():
        msg = f"The data in {file} doesn't exist."
        raise FileNotFoundError(msg)

    with open(file) as f:
        return json.load(f)


def mocked_requests_get(endpoint, *args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        @property
        def ok(self):
            return self.status_code == 200

    if "arrivals" in endpoint:
        file_name = "arrivals_response.json"
    elif "positions" in endpoint:
        file_name = "locations_response.json"
    elif "follow" in endpoint:
        file_name = "follow_response.json"

    data = load_test_data(file_name=file_name)

    return MockResponse(data, 200)


@pytest.fixture
def cta_client(mocker):
    mocker.patch("requests.get", side_effect=mocked_requests_get)

    return CTAClient(key=FAKE_KEY)


def test_attributes(cta_client):
    assert cta_client.version == 1
    assert cta_client.base_url == "http://lapi.transitchicago.com/api/1.0"


@pytest.mark.parametrize(
    "kwargs, error_type",
    [
        ({}, RequiredArgMissingError),
        ({"mapid": [1, 2, 3, 4, 5]}, TooManyArgsError),
        ({"stpid": [1, 2, 3, 4, 5]}, TooManyArgsError),
    ],
)
def test_arrivals_throws_error(cta_client, kwargs, error_type):
    with pytest.raises(error_type):
        cta_client.arrivals(**kwargs)


def test_arrivals(cta_client):
    arrivals_response = cta_client.arrivals(mapid=1)

    assert isinstance(arrivals_response, ArrivalResponse)
    df_arrivals = arrivals_response.to_frame()
    assert isinstance(df_arrivals, pd.DataFrame)
    assert len(df_arrivals) == 4

    cols = [
        "staId",
        "stpId",
        "staNm",
        "stpDe",
        "rn",
        "rt",
        "trDr",
        "prdt",
        "arrT",
        "isApp",
        "isSch",
        "isDly",
        "isFlt",
        "flags",
        "lat",
        "lon",
        "heading",
    ]
    for col in cols:
        assert col in df_arrivals


def test_locations(cta_client):
    locations_response = cta_client.locations(route=Route.BLUE)

    assert isinstance(locations_response, LocationResponse)
    df_locations = locations_response.to_frame()
    assert isinstance(df_locations, pd.DataFrame)
    assert len(df_locations) == 10

    cols = [
        "rn",
        "destSt",
        "destNm",
        "trDr",
        "nextStaId",
        "nextStpId",
        "nextStaNm",
        "prdt",
        "arrT",
        "isApp",
        "isDly",
        "flags",
        "lat",
        "lon",
        "heading",
    ]
    for col in cols:
        assert col in df_locations


def test_follow(cta_client):
    follow_response = cta_client.follow(runnumber=106)

    assert isinstance(follow_response, FollowResponse)
    df_follow = follow_response.to_frame()
    assert isinstance(df_follow, pd.DataFrame)
    assert len(df_follow) == 6
    cols = [
        "staId",
        "stpId",
        "staNm",
        "stpDe",
        "rn",
        "rt",
        "destSt",
        "destNm",
        "trDr",
        "prdt",
        "arrT",
        "isApp",
        "isSch",
        "isDly",
        "isFlt",
        "flags",
    ]
    for col in cols:
        assert col in df_follow
