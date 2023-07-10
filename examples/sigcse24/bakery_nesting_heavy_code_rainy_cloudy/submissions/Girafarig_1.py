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

def get_reports(forecasts: list[Forecast]) -> list[Report]:
    reports = []
    for forecast in forecasts:
        for report in forecast.reports:
            reports.append(report)
    return reports
    
def rainiest_cloudy(forecasts: list[Forecast]) -> bool:
    reports = get_reports(forecasts)
    if not forecasts:
        return False
    max_rainfall = reports[0].rainfall[0].amount
    most_rainy_report = reports[0]
    for report in reports:
        print(type(report))
        for measurement in report.rainfall:
            if measurement.amount > max_rainfall:
                max_rainfall = measurement.amount
                most_rainy_report = report
    return most_rainy_report.weather.cloudy

reports1 = [Report(52, [Measurement(2, True)], WeatherOptions(True, True, False))]
forecast1 = Forecast('Here', '12:00', reports1)
forecasts1 = [forecast1]

assert_equal(rainiest_cloudy([forecast1]), True)