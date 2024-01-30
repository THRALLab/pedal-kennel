from dataclasses import dataclass
from bakery import assert_equal

@dataclass
class Turtle:
    speed: int 
    direction: int

def point_turtle(ogTurtle: Turtle, newDirection: int):
    return Turtle(ogTurtle.speed, newDirection)

assert_equal(point_turtle(Turtle(10, 5), 10), Turtle(10, 10)