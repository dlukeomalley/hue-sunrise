import unittest
import config
import datetime
from dateutil.parser import parse
import sunrise
import requests

class Test(unittest.TestCase):
  # TODO (dlukeomalley): get schedule and save to rewrite it later
  testScheduleId = config.SCHEDULE_ID
  testLocation = (37.7749, -122.4194)
  testDate = datetime.date(2020, 4, 27)
  testSunriseDt = parse("2020-04-27 13:16:53+00:00")
  localtimeString = "/schedules/{}/localtime".format(testScheduleId)  

  def test_get_sunrise_sunset(self):
    self.assertEqual(self.testSunriseDt, sunrise.getSunriseDatetime(self.testDate, self.testLocation))

  def test_timezone_change(self):
    timezone = "US/Pacific"
    sunriseTime = self.testSunriseDt - datetime.timedelta(hours=7)
    self.assertEqual(sunriseTime.ctime(), sunrise.getSunriseDatetime(self.testDate, self.testLocation, timezone).ctime())

  def test_one_time_alarm(self):
    success = {"success": {self.localtimeString: "2020-04-27T13:16:53"}}
    self.assertIn(success, sunrise.setHueSchedule(self.testScheduleId, self.testSunriseDt))

  def test_recurring_alarm(self):
    recurrence = 0b01111111 # 127
    success = {"success": {self.localtimeString: "W127/T13:16:53"}}
    self.assertIn(success, sunrise.setHueSchedule(self.testScheduleId, self.testSunriseDt, recurrence))

if __name__ == '__main__':
    unittest.main()