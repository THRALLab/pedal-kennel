from dataclasses import dataclass
from bakery import assert_equal

@dataclass
class Turtle:
    speed: int
    direction: int
    
def point_turtle(t: Turtle, integer: int) -> Turtle:
    t.direction = integer
    return Turtle(t.speed, t.direction)

assert_equal(point_turtle(Turtle(10,20),10), Turtle(10,10))
assert_equal(point_turtle(Turtle(20,20),10), Turtle(20,10))