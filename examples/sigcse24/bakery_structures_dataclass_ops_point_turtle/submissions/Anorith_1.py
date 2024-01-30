from dataclasses import dataclass
from bakery import assert_equal

@dataclass
class Turtle:
    speed: int
    direction: int

def point_turtle(turt: Turtle, direct: int) -> Turtle:
    turt.direction = direct
    return turt

assert_equal(point_turtle(Turtle(2, 1), 3), Turtle(2, 3))
assert_equal(point_turtle(Turtle(3, 1), 3), Turtle(3, 3))
assert_equal(point_turtle(Turtle(4, 1), 3), Turtle(4, 3))