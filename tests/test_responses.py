import pytest

from cta.responses import (
    ArrivalResponse,
    LocationResponse,
    FollowResponse,
    NoTrainsError,
)


dummy_train_data_1 = {
    "rn": "106",
    "destSt": "30171",
    "destNm": "O'Hare",
    "trDr": "1",
    "nextStaId": "40590",
    "nextStpId": "30115",
    "nextStaNm": "Damen",
    "prdt": "2022-05-15T15:20:41",
    "arrT": "2022-05-15T15:22:41",
    "isApp": "0",
    "isDly": "0",
    "flags": None,
    "lat": "41.90336",
    "lon": "-87.6665",
    "heading": "303",
}

dummy_train_data_2 = {
    "rn": "107",
    "destSt": "30171",
    "destNm": "O'Hare",
    "trDr": "1",
    "nextStaId": "40010",
    "nextStpId": "30001",
    "nextStaNm": "Austin",
    "prdt": "2022-05-15T15:21:04",
    "arrT": "2022-05-15T15:22:04",
    "isApp": "1",
    "isDly": "0",
    "flags": None,
    "lat": "41.87166",
    "lon": "-87.78649",
    "heading": "95",
}

blue_line_route_data = [
    {"@name": "blue", "train": [dummy_train_data_1, dummy_train_data_2]}
]

yellow_line_single_data = [{"@name": "y", "train": dummy_train_data_1}]


@pytest.mark.parametrize(
    "route_data, data_len",
    [
        (blue_line_route_data, 2),
        # seems if one trains running... not a list
        (yellow_line_single_data, 1),
        (blue_line_route_data + yellow_line_single_data, 3),
    ],
)
def test_locations_init(route_data, data_len):
    data = {"ctatt": {"route": route_data, "errCd": "0"}}
    locations_response = LocationResponse(data=data)

    df_locations = locations_response.to_frame()
    assert len(df_locations) == data_len

    for col in ["mins_til_arrival", "mins_since_prediction"]:
        assert col in df_locations


def test_locations_no_trains():
    data = {"ctatt": {"route": [{"@name": "yellow"}], "errCd": 0}}

    locations_response = LocationResponse(data=data)

    with pytest.raises(NoTrainsError):
        locations_response.to_frame()


@pytest.mark.parametrize("cls", [ArrivalResponse, FollowResponse, LocationResponse])
def test_error_on_init(cls):
    data = {"ctatt": {"errCd": "105", "errNm": "Some error from the api"}}
    with pytest.raises(ValueError):
        cls(data=data)


@pytest.mark.parametrize("cls", [ArrivalResponse, FollowResponse])
def test_arrival_and_follow_no_trains(cls):
    data = {
        "ctatt": {
            "errCd": "0",
        }
    }

    response = cls(data=data)

    with pytest.raises(NoTrainsError):
        response.to_frame()
