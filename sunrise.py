#!/usr/bin/env python

import config
import requests
from datetime import date, timedelta
from dateutil.parser import parse
import pytz

def getSunriseDatetime(date, location, tzinfo="UTC"):
	# Sunrise Sunset provides our sunrise and sunset times: http://sunrise-sunset.org/api
	lat, lng = location
	sunJson = requests.get("http://api.sunrise-sunset.org/json?lat={}&lng={}&date={}&formatted=0".format(lat, lng, date)).json()
	sunriseTimeString = sunJson['results']['sunrise']

	# Sample sunriseTimeString: 2016-04-21T13:24:28+00:00
	sunriseDt = parse(sunriseTimeString)
	return sunriseDt.astimezone(pytz.timezone(tzinfo))

def getBaseUrl():
	return "http://{ip}/api/{token}".format(ip=config.IP, token=config.USER_TOKEN)

def setHueSchedule(scheduleId, dT, recurrence=None):
	url = "{baseUrl}/schedules/{scheduleId}".format(baseUrl=getBaseUrl(), scheduleId=scheduleId)
	formattedTime = None
	time = dT.strftime("%H:%M:%S")
	if recurrence:
		formattedTime = "W{}/T{}".format(recurrence, time)
	else:
		formattedTime = "{}T{}".format(dT.date(), time)

	payload = {"name":"[{}] Sunrise Alarm".format(dT.date()), "localtime":formattedTime}
	result = requests.put(url, json=payload)
	return result.json()
	
def main():
	tomorrow = date.today() + timedelta(days=1)
	sunriseDt = getSunriseDatetime(tomorrow, config.LOCATION, config.TIMEZONE)
	setHueSchedule(config.SCHEDULE_ID, sunriseDt)

if __name__ == "__main__":
	main()