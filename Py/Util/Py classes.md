
__new__()

__init__()

__metaclass__

__call__()


__iter__()

__str__()  
 - returns a user friendly representation of an object

__repr__()  
- returns a developer friendly representation of an object (e.g dataclasses)

__cmp__()


### Dataclasses
````python
from dataclasses import dataclass
from typing import Any

@dataclass
class WithoutExplicitTypes:
    name: Any
    value: Any = 42
````
Advanced default values
````python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Deck:
    cards: List[PlayingCard] = field(default_factory=make_french_deck)
````
The field() specifier is used to customize each field of a data class individually
- default: Default value of the field
- default_factory: Function that returns the initial value of the field
- init: Use field in .__init__() method? (Default is True.)
- repr: Use field in repr of the object? (Default is True.)
- compare: Include the field in comparisons? (Default is True.)
- hash: Include the field when calculating hash()? (Default is to use the same as for compare.)
- metadata: A mapping with information about the field. e.g for 3rd party tools

The metadata (and other information about a field) can be retrieved using the fields() function:
````python
from dataclasses import fields
fields(Position)
````

How to overwrite the __repr__() function to show a more friendly version of the dataclass content
````python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Deck:
    cards: List[PlayingCard] = field(default_factory=make_french_deck)

    def __repr__(self):
        cards = ', '.join(f'{c!s}' for c in self.cards)
        return f'{self.__class__.__name__}({cards})'
````

The @dataclass decorator can have parameters
 
init: Add .__init__() method? (Default is True.)
repr: Add .__repr__() method? (Default is True.)
eq: Add .__eq__() method? (Default is True.)
order: Add ordering methods? (Default is False.)
unsafe_hash: Force the addition of a .__hash__() method? (Default is False.)
frozen: If True, assigning to fields raise an exception. (Default is False.)

````python
from dataclasses import dataclass, field

RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()
SUITS = '♣ ♢ ♡ ♠'.split()

@dataclass(order=True)
class PlayingCard:
    # add sort_index field for sorting. the fields are compared in order
    # not initialized in the constructor
    # removed from repr, for not confusing the user
    sort_index: int = field(init=False, repr=False)
    rank: str
    suit: str

    def __post_init__(self):
        self.sort_index = (RANKS.index(self.rank) * len(SUITS)
                           + SUITS.index(self.suit))

    def __str__(self):
        return f'{self.suit}{self.rank}'
````

