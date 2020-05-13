At its core, Cython is an intermediate step between Python and C/C++. It allows you to write pure Python code with some minor modifications, which is then translated directly into C code.

https://towardsdatascience.com/use-cython-to-get-more-than-30x-speedup-on-your-python-code-f6cb337919b6

#### range
````python 
import sys


# range function returns a class that only behaves like a list. 
# A range is a lot more memory efficient than using an actual list of numbers
mylist = range(0, 10000)
print(sys.getsizeof(mylist))
# 48

myreallist = [x for x in range(0, 10000)]
print(sys.getsizeof(myreallist))
# 87632
````

#### functions

Functions in Python can return more than one variable without the need for a dictionary, a list or a class
````python
def get_user(id):
    # fetch user from database
    # ....
    return name, birthdate

name, birthdate = get_user(4)
````

