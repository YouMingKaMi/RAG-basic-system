def add(a, b):
    c = a+b
    return c

def test_add():
    assert add(2,3) == 5, "Wrong"

test_add()