# Chicago Train API

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

## Getting Started

```python
from cta import CTAClient
damen_blue_line_mapid = 40590

# Get arrival information for damen blue line station.
cta = CTAClient()
arrival_response = cta.arrivals(mapid=damen_blue_line_mapid)
df_arrivals = arrival_response.to_frame()
print(df_arrivals)

# Follow specific train
runnumber = df_arrivals["rn"].tolist()[0]
follow_response = cta.follow(runnumber=runnumber)
df_follow = follow_response.to_frame()
print(df_follow)
```

```python
from cta import Route

# Get the location of all Blue Line trains.
location_response = cta.locations(Route.BLUE)
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

df_damen = stations.lookup("Damen")
print(df_damen)
```
