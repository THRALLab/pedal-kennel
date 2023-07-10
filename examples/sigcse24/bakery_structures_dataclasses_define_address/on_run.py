from pedal import *
from curriculum_sneks import *
from dataclasses import dataclass

@dataclass
class Address:
    number: int
    street: str
    city: str
    state: str

ensure_dataclass(Address, priority='instructor')
assert_is_instance(evaluate("Address"), type)
ensure_function_call('Address', 1)

check_dataclass_instance(evaluate('location'), Address)
assert_equal(evaluate('location'), call("Address", 18, "Amstel Ave", "Newark", "DE"))

ensure_ast('Attribute')

assert_output_contains(student, "DE")