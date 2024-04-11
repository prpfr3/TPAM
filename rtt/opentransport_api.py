# Reading Data from TransportAPI https://developer.transportapi.com/
# Live Times https://developer.transportapi.com/docs?raml=https://transportapi.com/v3/raml/transportapi.raml##uk_train_station_station_code_live_json

import requests
from django.conf import settings


def otapi_location(location):
    url = "http://transportapi.com/v3/uk/places.json?query={}&type={}&app_id={}&app_key={}".format(
        location, location_type, settings.OTAPI_APP_ID, settings.OTAPI_API_KEY
    )
    r = requests.get(url)
    return r.json()


def otapi_timetable(station_code):
    url = "http://transportapi.com/v3//uk/train/station/{}/{}/{}/timetable.json?app_id={}&app_key={}".format(
        station_code,
        live_date,
        live_time,
        settings.OTAPI_APP_ID,
        settings.OTAPI_API_KEY,
    )
    r = requests.get(url)
    return r.json()


def otapi_livefreight(station_code):
    train_status = "freight"  # can be passenger or freight, not both
    url = "http://transportapi.com/v3//uk/train/station/{}/live.json?app_id={}&app_key={}&train_status={}&type={}".format(
        station_code, settings.OTAPI_APP_ID, settings.OTAPI_API_KEY, train_status, type
    )
    r = requests.get(url)
    return r.json()


def otapi_livepassenger(station_code):
    train_status = "passenger"  # can be passenger or freight, not both
    url = "http://transportapi.com/v3//uk/train/station/{}/live.json?app_id={}&app_key={}&train_status={}&type={}".format(
        station_code, settings.OTAPI_APP_ID, settings.OTAPI_API_KEY, train_status, type
    )
    r = requests.get(url)
    return r.json()


def otapi_service(train_uid):
    service = "train_uid:" + train_uid
    url = "http://transportapi.com/v3//uk/train/service/{}/timetable.json?app_id={}&app_key={}&darwin={}&live={}&stop_type={}".format(
        service, settings.OTAPI_APP_ID, settings.OTAPI_API_KEY, darwin, live, stop_type
    )
    r = requests.get(url)
    return r.json()


live_date = ""
live_time = ""
location_type = "train_station"
type = "arrival,departure,pass"  # can be one or all
stop_type = "arrival,departure,pass"  # can be one or all
# service = 'service:51464580' #Can be train_uid:
# service = 'train_uid:H08263' #Can be train_uid:
darwin = "true"
live = "true"
# atcocode = '490012247A'

if __name__ == "__main__":
    otapi_timetable()
