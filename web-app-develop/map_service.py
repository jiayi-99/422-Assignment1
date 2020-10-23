import requests
from pprint import pprint
import json

OPEN_ROUTE_API_KEY = '5b3ce3597851110001cf62485788356becfe4894aba648ee6673baab'

def get_map_data(source_cor, destination_cor):
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    }
    url = 'https://api.openrouteservice.org/v2/directions/driving-car?api_key=' + OPEN_ROUTE_API_KEY + \
        '&start={slat},{slon}&end={dlat},{dlon}'.format(slat=source_cor[0], slon=source_cor[1],\
        dlat=destination_cor[0], dlon=destination_cor[1])
    print(url)
    call = requests.get(
        url,
        headers=headers
    )

    print(call.status_code, call.reason)
    return json.loads(call.text)


if __name__ == '__main__':
    pprint(get_map_data(
        source_cor=['8.681495','49.41461'],
        destination_cor=['8.687872','49.420318']
    ))