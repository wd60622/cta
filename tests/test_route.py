from cta import route

import pytest


@pytest.mark.parametrize(
    "route_name, value",
    [
        ("RED", "red"),
        ("BLUE", "blue"),
        ("GREEN", "g"),
        ("ORANGE", "org"),
        ("PURPLE", "p"),
        ("PINK", "pink"),
        ("YELLOW", "y"),
    ],
)
def test_valid_routes(route_name, value):
    rt = getattr(route.Route, route_name)
    assert rt.name == route_name
    assert rt.value == value


@pytest.mark.parametrize(
    "invalid_name",
    [
        "red",
        "blue",
        "green",
        "orange",
        "purple",
        "pink",
        "yellow",
    ],
)
@pytest.mark.parametrize("method", ["lower", "title"])
def test_invalid_routes(invalid_name, method):
    with pytest.raises(AttributeError):
        getattr(route.Route, getattr(invalid_name, method)())
