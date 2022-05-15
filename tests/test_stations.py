import pandas as pd

import pytest

from cta import Stations

from pathlib import Path


TEST_DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture
def stations():
    Stations.url = TEST_DATA_DIR / "stations.json"
    return Stations()


def test_stations(stations):
    assert isinstance(stations.data, pd.DataFrame)
    assert len(stations.lookup("18th")) == 2
