from bakery import assert_equal

def dispatch_math(operator: str, a : int, b : int) -> int:
    if '+-/*' not in operator:
        return 0
    if operator == '/' and b == 0:
        return 0
    return (a + operator + b) 
    
assert_equal(dispatch_math('&', 1, 0), 0)
assert_equal(dispatch_math('*', 1, 0), 0)
assert_equal(dispatch_math('/', 2, 2), 1)