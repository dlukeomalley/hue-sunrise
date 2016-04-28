#!/usr/bin/env python

import config
import requests
from datetime import date, timedelta
from dateutil.parser import parse
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

def setHueSchedule(days, time):
	url = "http://{ip}/api/{token}/schedules/{scheduleId}".format(scheduleId=config.SCHEDULE_ID, \
																          ip=config.IP,          \
																       token=config.USER_TOKEN)
	
	formattedTime = "W{}/T{}".format(days, time.strftime("%H:%M:%S"))
	payload = {"name":"[{}] Sunrise Alarm".format(time.date()), "localtime":formattedTime}
	result = requests.put(url, json=payload)
	return results.json
	
def main():
	tomorrow = date.today() + timedelta(days=1)
	# Lat & Long for San Francisco, CA, USA are 37.7749, -122.4194
	sunriseDt = getSunriseDatetime(tomorrow, (37.7749, -122.4194), 'US/Pacific')
	
	setHueSchedule(0b1111111, sunriseDt)

if __name__ == "__main__":
	main()
	