from dataclasses import dataclass
from bakery import assert_equal

@dataclass
class WeatherOptions:
    raining: bool
    cloudy: bool
    snowing: bool  

@dataclass
class Measurement:
    amount: int
    automatic: bool
    
@dataclass
class Report:
    temperature: int
    rainfall: list[Measurement]
    weather: WeatherOptions

@dataclass
class Forecast:
    when: str
    where: str
    reports: list[Report]
    
def rainiest_cloudy(forecasts: list[Forecast]) -> bool:
    rainfall = False
    max_rain = 0
    for forecast in forecasts:
        reportlist = forecast.reports
        for report in reportlist:
            rainlist = report.rainfall
            for rain in rainlist:
                if rain.amount > max_rain:
                    max_rain = rain.amount
                    max_day = report
    if report.weather.cloudy:
        rainfall = True
    return rainfall            



today = Forecast("today", "Newark, DE", [
    Report(54, [Measurement(1, True), Measurement(2, True)],
        WeatherOptions(True, True, False)),
    Report(65, [Measurement(2, True)],
        WeatherOptions(True, True, False)),
    Report(45, [],
        WeatherOptions(False, True, False))
])
tomorrow = Forecast("tomorrow", "Newark, DE", [
    Report(54, [Measurement(1, True), Measurement(1, True)],
        WeatherOptions(True, True, False)),
    Report(65, [Measurement(3, True), Measurement(5, True), Measurement(10, False)],
        WeatherOptions(True, True, True)),
    Report(45, [Measurement(20, True)],
        WeatherOptions(True, False, False))
])

soon = Forecast("soon", "Newark, DE", [
    Report(14, [Measurement(5, False)],
        WeatherOptions(False, True, True))
])

assert_equal([today, tomorrow], 0)
assert_equal([soon], 0)

    
