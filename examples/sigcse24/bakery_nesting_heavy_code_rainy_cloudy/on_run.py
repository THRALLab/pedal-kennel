from pedal import *
from curriculum_sneks import *
from dataclasses import dataclass

from dataclasses import dataclass

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
    
CLASSES = [Forecast, Report, Measurement, WeatherOptions]
NAMES = ["Forecast", "Report", "Measurement", "WeatherOptions"]


prevent_printing_functions()
ensure_functions_return()

for name, dc in zip(NAMES, CLASSES):
    ensure_dataclass(dc, priority='instructor')
    assert_is_instance(evaluate(name), type)

ensure_function('rainiest_cloudy', 1, ['list[Forecast]'], bool)
ensure_function_callable('rainiest_cloudy')

ensure_coverage(.9)
ensure_cisc108_tests(2)

for name in NAMES:
    ensure_function_call(name, 2)
ensure_called_uniquely('rainiest_cloudy', 2)

context = run("""today = Forecast("today", "Newark, DE", [
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
empty = Forecast("empty", "Newark, DE", [])
""")

unit_test('rainiest_cloudy', 
          ('[]', False),
          ('[empty]', False),
          ('[today]', True),
          ('[tomorrow]', False),
          ('[soon]', True),
          ('[today, tomorrow]', False),
          ('[today, tomorrow, soon]', False),
          ('[soon, soon, soon, soon, soon]', True),
          context=context
)

