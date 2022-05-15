# Chicago Transit Authority API

The CTA has three public endpoints for tracking CTA trains. This client supports
those endpoints.

The `CTAClient` has methods for each endpoints. Namely,
- arrivals: Arrival information for a given station(s) or stop(s).
- follow: Follow specific train by runnumber.
- locations: Get all trains for a given route(s).

More endpoint specific documentation found [here](
https://www.transitchicago.com/developers/ttdocs/)

This API requires a key which can be easily received [here](https://www.transitchicago.com/developers/traintrackerapply/).
Follow the `.env.example` file for setting.

## Installation

This package is available on `pip`. Install with:

```bash
$ pip install python-cta
```

## Getting Started

```python
from cta import CTAClient
damen_blue_line_mapid = 40590

# Get arrival information for damen blue line station.
cta_client = CTAClient()
arrival_response = cta_client.arrivals(mapid=damen_blue_line_mapid)
df_arrivals = arrival_response.to_frame()
print(df_arrivals)

# Follow specific train
runnumber = df_arrivals["rn"].tolist()[0]
follow_response = cta_client.follow(runnumber=runnumber)
df_follow = follow_response.to_frame()
print(df_follow)
```

```python
from cta import Route

# Get the location of all Blue Line trains.
location_response = cta_client.locations(Route.BLUE)
df_locations = location_response.to_frame()
print(df_locations)

# Or all trains on the track
location_response = cta_client.locations(route=[route for route in Route])
df_locations = location_response.to_frame()
print(df_locations)
```

Information about the stations can be found with the `Stations` class. Below is an
example to find the mapid for Damen blue line.

```python
from cta import Stations

stations = Stations()
df_stations = stations.data
print(df_stations)

df_damen = stations.lookup("Damen", route=Route.BLUE)
print(df_damen)
```

Try this example for yourself in `scripts/readme_example.py`
