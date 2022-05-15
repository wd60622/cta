import pytest

from cta.client import (
    ParamBuilder,
    CTAClient,
    RequiredArgMissingError,
    TooManyArgsError,
)
from cta import Route


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
            {"mapid": 1, "stpid": 1},
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


@pytest.fixture
def cta_client(mocker):
    return CTAClient(key=FAKE_KEY)


def test_attributes(cta_client):
    assert cta_client.version == 1
    assert cta_client.base_url == "http://lapi.transitchicago.com/api/1.0"


@pytest.mark.parametrize(
    "kwargs, error_type",
    [({}, RequiredArgMissingError), ({"mapid": [1, 2, 3, 4, 5]}, TooManyArgsError)],
)
def test_arrivals_both_none(cta_client, kwargs, error_type):
    with pytest.raises(error_type):
        cta_client.arrivals(**kwargs)
