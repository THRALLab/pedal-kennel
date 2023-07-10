from dataclasses import dataclass 
from bakery import assert_equal 

@dataclass
class Measurement: 
    amount: int
    automatic: bool 

@dataclass
class WeatherOptions: 
    raining: bool 
    cloudy: bool 
    snowing: bool 
    
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
    
forecasts = [Forecast("Night", "Delaware", [Report(54, [Measurement(2, True), Measurement(1, False)], WeatherOptions(True, True, False))]),
            Forecast("Day", "New York", [Report(32, [Measurement(0, True), Measurement(1, True)], WeatherOptions(False, True, True))])] 

forecasts_2 = [Forecast("Night", "Delaware", [Report(54, [Measurement(6, True), Measurement(4, False)], WeatherOptions(True, True, False))]),
            Forecast("Day", "New York", [Report(32, [Measurement(3, True), Measurement(2, True)], WeatherOptions(True, True, False))])] 

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

empty = Forecast("empty", "Newark, DE", [] )   
    
def rainiest_cloudy (forecasts: list[Forecast]) -> bool:
    max_rain = 0
    is_cloudy = False
    for forecast in forecasts:
        for report in forecast.reports:
            if report.weather.cloudy == True:
                for rainfall in report.rainfall:
                    if rainfall.amount > max_rain:
                        max_rain = rainfall.amount
                        is_cloudy = True
            else:
                is_cloudy = False
    return is_cloudy
                    

assert_equal(rainiest_cloudy([empty, empty]), False)
assert_equal(rainiest_cloudy([today]), True)
assert_equal(rainiest_cloudy([tomorrow]), False)



           
           
        