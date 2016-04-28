import unittest
import datetime
from dateutil.parser import parse
import sunrise

class TestSunrise(unittest.TestCase):

  def test_get_sunrise_sunset(self):
    date = datetime.date(2016, 4, 27)
    location = (37.7749, -122.4194)

    sunriseTime = parse("2016-04-27 13:16:55+00:00")
    self.assertEqual(sunriseTime, sunrise.getSunriseDatetime(date, location))

  def test_timezone_change(self):
    date = datetime.date(2016, 4, 27)
    location = (37.7749, -122.4194)
    timezone = "US/Pacific"

    sunriseTime = parse("2016-04-27 13:16:55+00:00")
    # Adjust UTC to US/Pacific timezone
    sunriseTime -= datetime.timedelta(hours=7)
    
    self.assertEqual(sunriseTime.ctime(), sunrise.getSunriseDatetime(date, location, timezone).ctime())

if __name__ == '__main__':
    unittest.main()