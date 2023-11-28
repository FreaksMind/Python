def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if type(x) == int and type(y) == int:
        return x // y
    else:
        return x/y
