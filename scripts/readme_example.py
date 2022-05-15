from cta import CTAClient, Route, Stations


def train_endpoints_example(cta_client: CTAClient) -> None:
    damen_blue_line_mapid = 40590

    arrival_response = cta_client.arrivals(mapid=damen_blue_line_mapid)
    df_arrivals = arrival_response.to_frame()
    print(f"Arrival information for Damen Blue Line:")
    print(df_arrivals)

    for runnumber in df_arrivals["rn"].tolist():
        # Not always reliable. Try until one is successful
        try:
            follow_response = cta_client.follow(runnumber=runnumber)
        except ValueError as e:
            print(e)
            print(df_arrivals.loc[df_arrivals["rn"] == runnumber].T)
        else:
            break
    df_follow = follow_response.to_frame()
    print(
        f"Follow next few stops for Train ({runnumber = }) currently coming into Damen station:"
    )
    print(df_follow)

    blue_location_response = cta_client.locations(Route.BLUE)
    df_blue = blue_location_response.to_frame()
    print("Location of all Blue Line Trains:")
    print(df_blue)

    all_location_response = cta_client.locations([route for route in Route])
    df_all = all_location_response.to_frame()
    print("Location of all Trains:")
    print(df_all)


def station_example(stations: Stations) -> None:
    df_stations = stations.data
    print("All stations information")
    print(df_stations)

    df_damen = stations.lookup("Damen")
    print("'lookup' method for keyword 'Damen'")
    print(df_damen)

    df_damen_blue = stations.lookup("Damen", route=Route.BLUE)
    print("'lookup' method for keyword 'Damen' and route set to 'Route.BLUE'")
    print(df_damen_blue)


if __name__ == "__main__":
    cta_client = CTAClient()

    train_endpoints_example(cta_client=cta_client)

    stations = Stations()
    station_example(stations=stations)
