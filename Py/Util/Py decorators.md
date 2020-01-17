

# Python decorators

https://medium.com/better-programming/decorators-in-python-72a1d578eac4

## [Scenario 1]: wrap another function

``` python
import functools
import time

def timer(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print("Finished {} in {} secs".format(repr(func.__name__), round(run_time, 3)))
        return value

    return wrapper
	
# use the timer decorator	
@timer
def doubled_and_add(num):
    res = sum([i*2 for i in range(num)])
    print("Result : {}".format(res))

doubled_and_add(100000)
doubled_and_add(1000000)

```

Result:
```cmd
Result : 9999900000
Finished ‘doubled_and_add’ in 0.0119 secs
Result : 999999000000
Finished ‘doubled_and_add’ in 0.0897 secs
```
## [Scenario 2]: Lightweight plugins architecture

``` python
PLUGINS = dict()

def register(func):
    PLUGINS[func.__name__] = func
    return func

@register
def add(a, b):
    return a+b

@register
def multiply(a, b):
    return a*b

def operation(func_name, a, b):
    func = PLUGINS[func_name]
    return func(a, b)

print(PLUGINS)
print(operation('add', 2, 3))
print(operation('multiply', 2, 3))
```

## [Decorating classes]

``` python 
class Circle:
    def __init__(self, radius):
        self._radius = radius

    # property - used to customize getters and setters for class attributes
    @property
    def radius(self):
        """Get value of radius"""
        return self._radius

    # .radius is a mutable property: it can be set to a different value. 
    # However, by defining a setter method, we can do some error testing to make sure it’s not set to a nonsensical negative number. 
    # Properties are accessed as attributes without parentheses
    @radius.setter
    def radius(self, value):
        """Set radius, raise error if negative"""
        if value >= 0:
            self._radius = value
        else:
            raise ValueError("Radius must be positive")

    # .area is an immutable property: properties without .setter() methods can’t be changed. 
    # Even though it is defined as a method, it can be retrieved as an attribute without parentheses.
    @property
    def area(self):
        """Calculate area inside circle"""
        return self.pi() * self.radius**2

    # regular method
    def cylinder_volume(self, height):
        """Calculate volume of cylinder with circle as base"""
        return self.area * height

    # Class methods are often used as factory methods that can create specific instances of the class
    # It’s not bound to a particular instance of Circle. 
    @classmethod
    def unit_circle(cls):
        """Factory method creating a circle with radius 1"""
        return cls(1)

    # Static methods can be called on either an instance or the class
    @staticmethod
    def pi():
        """Value of π, could use math.pi instead though"""
        return 3.1415926535

    # using the previously defined decorator for a class method
    @timer
    def somemethod(self):
        print("Area is: " self.area)

```

Decorating a class does not decorate its methods. Below, @timer only measures the time it takes to instantiate the class.

``` python
@timer
class Calculator:
    ....

c = Calculator(100)    
```
will output:
```bat
Finished 'Calculator' in 2.001 secs
```

## [Nesting decorators]

```python
def hello(func):
    def wrapper():
        print("Hello")
        func()
    return wrapper

def welcome(func):

    def wrapper():
        print("Welcome")
        func()
    return wrapper

@hello
@welcome
def say():
    print("Greeting Dome")

say()
```

Output:

```cmd
Hello
Welcome
Greeting Dome
```

Decorators are being executed in the order they’re listed. In other words, @hello calls @welcome, which calls say().

## [Decorators With Arguments]

```python
def repeat(*args_, **kwargs_):

    def inner_function(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(args_[0]):
                func(*args, **kwargs)
        return wrapper

    return inner_function


@repeat(4)
def say(name):
    print(f"Hello {name}")

say("World")
```

Output:

```cmd
Hello World
Hello World
Hello World
Hello World
```

## [ Stateful Decorators ]

We can use a decorator to keep track of state. As a simple example, we will create a decorator that counts the number of times a function is called.

```python
def count_calls(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.num_calls += 1
        print(f"Call {wrapper.num_calls} of {func.__name__!r}")
        return func(*args, **kwargs)

    wrapper.num_calls = 0
    return wrapper


@count_calls
def say():
    print("Hello!")

say()
say()
say()
say()
print(say.num_calls)
```

Output:

```
Call 1 of 'say'
Hello!
Call 2 of 'say'
Hello!
Call 3 of 'say'
Hello!
Call 4 of 'say'
Hello!
4
```

## [ Classes as Decorators ]

If we want to use class as a decorator it needs to take func as an argument in its .__init__() method.  
Furthermore, the class needs to be callable so that it can stand in for the decorated function. For a class to be callable, you implement the special .__call__() method.

```python
class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f"Call {self.num_calls} of {self.func.__name__!r}")
        return self.func(*args, **kwargs)


@CountCalls
def say():
    print("Hello!")

say()
say()
say()
say()
print(say.num_calls)
```

## [ Class-Based Decorators with Arguments ]

```python
class ClassDecorator(object):

    def __init__(self, arg1, arg2):
        print("Arguements of decorator %s, %s" % (arg1, arg2))
        self.arg1 = arg1
        self.arg2 = arg2

    def __call__(self, func):
        functools.update_wrapper(self, func)

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

@ClassDecorator("arg1", "arg2")
def print_args(*args):
    for arg in args:
        print(arg)

print_args(1, 2, 3)
```

Output
```cmd
Arguments of decorator arg1, arg2
1
2
3
```