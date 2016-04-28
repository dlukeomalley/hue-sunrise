#!/usr/bin/env python

import requests
from dateutil.parser import parse
from datetime import date, timedelta
import pytz

def getSunriseDatetime(date, location, tzinfo="UTC"):
	# Sunrise Sunset provides our sunrise and sunset times: http://sunrise-sunset.org/api
	# We calculate the explicit date to avoid timezone issues with the api provider
	lat, lng = location
	sunJson = requests.get("http://api.sunrise-sunset.org/json?lat={}&lng={}&date={}&formatted=0".format(lat, lng, date)).json()
	sunriseTimeString = sunJson['results']['sunrise']

	# Sample sunriseTimeString: 2016-04-21T13:24:28+00:00
	sunriseDt = parse(sunriseTimeString)
	return sunriseDt.astimezone(pytz.timezone(tzinfo))

def main():
	hueToken = "DfVZeleoILd4pIe2ZvM2UfVCcea9OiBbH8biB49b"
	alarmId = "0415713780126651"
	hueIp = "192.168.1.137"
	hueUrl = "http://{}/api/{}/schedules/{}".format(hueIp, hueToken, alarmId)

	weekBitmask = 124

	# Lat & Long for San Francisco, CA, USA are 37.7749, -122.4194
	tomorrow = date.today() + timedelta(days=1)
	sunriseDt = getSunriseDatetime(tomorrow, (37.7749, -122.4194), 'US/Pacific')
	hueTime = "W{}/T{}".format(weekBitmask, sunriseDt.strftime("%H:%M:%S"))
	
	payload = {"name":"[{}] Sunrise Alarm".format(sunriseDt.date()), "localtime":hueTime}
	result = requests.put(hueUrl, json=payload)
	print result.json()

if __name__ == "__main__":
    main()