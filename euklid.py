from copy import copy
from dataclasses import dataclass, field, asdict
from math import gcd
from typing import Iterator, Iterable

from tabulate import tabulate


@dataclass()
class Euclid(Iterable):
    # Only kept for validation
    _a: int = field(init=False)
    _b: int = field(init=False)

    x: int
    y: int
    q: int = field(init=False)
    r: int = field(init=False)
    u: int = 1
    s: int = 0
    v: int = 0
    t: int = 1

    def __post_init__(self) -> None:
        if self.x <= 0 or self.y <= 0 or self.x == self.y:
            raise ValueError("The numbers must not be 0, negative, or equal to one another")

        self._a = self.x
        self._b = self.y

        self.q = self.x // self.y
        self.r = self.x - self.q * self.y

    def __iter__(self) -> Iterator['Euclid']:
        return self

    def __next__(self) -> 'Euclid':
        if self._is_done():
            self._assert_final()
            raise StopIteration

        self._shift()
        self.assert_row()
        return self

    def _shift(self) -> None:
        old: Euclid = copy(self)
        self.x = old.y
        self.y = old.r
        self.q = self.x // self.y
        self.r = self.x - self.q * self.y
        self.u = old.s
        self.s = old.u - old.q * old.s
        self.v = old.t
        self.t = old.v - old.q * old.t

    def assert_row(self) -> None:
        assert self.r == self.x % self.y
        assert self.y == self.s * self._a + self.t * self._b

    def _assert_final(self) -> None:
        assert self.y == gcd(self._a, self._b)
        if self.y == 1:
            assert (self.t * self._b) % self._a == 1

    def _is_done(self) -> bool:
        return self.r == 0

    def dict(self) -> dict:
        """Filter fields that start with a _"""
        return {key: value for (key, value) in asdict(self).items() if not key.startswith("_")}

    @staticmethod
    def print_table(a: int, b: int):
        euclid = Euclid(a, b)
        rows = [euclid.dict()]
        for row in euclid:
            rows.append(row.dict())

        print(tabulate(rows, headers="keys", showindex=True))
        print(f"==> The GCD of {a} and {b} is {euclid.y}")
