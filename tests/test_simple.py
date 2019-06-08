from math import gcd

import pytest

from euklid import Euclid


def assert_values(row: Euclid, x, y, q, r, u, s, v, t) -> bool:
    return row.x == x and \
           row.y == y and \
           row.q == q and \
           row.r == r and \
           row.u == u and \
           row.s == s and \
           row.v == v and \
           row.t == t


class TestConstructor:
    def test_a_0(self):
        with pytest.raises(ValueError):
            Euclid(0, 1)

    def test_b_0(self):
        with pytest.raises(ValueError):
            Euclid(1, 0)

    def test_a_equal_b(self):
        with pytest.raises(ValueError):
            value = 5
            Euclid(value, value)

    def test_default_values(self):
        a = 10
        b = 2
        q = a // b
        row = Euclid(10, 2)
        assert row.x == a
        assert row.x == row.q * row.y + row.r
        assert row.y == b
        assert row.q == q
        assert row.r == a - q * b
        assert row.u == row.t == 1
        assert row.s == row.v == 0


class TestIterator:
    def test_iterator(self):
        row = Euclid(99, 79)
        assert assert_values(row, 99, 79, 1, 20, 1, 0, 0, 1)
        row = next(row)
        assert assert_values(row, 79, 20, 3, 19, 0, 1, 1, -1)
        row = next(row)
        assert assert_values(row, 20, 19, 1, 1, 1, -3, -1, 4)
        row = next(row)
        assert assert_values(row, 19, 1, 19, 0, -3, 4, 4, -5)
        with pytest.raises(StopIteration):
            next(row)
        # the protocol says, it must raise it subsequently
        with pytest.raises(StopIteration):
            next(row)


class TestBug:
    def test_bug(self):
        row = Euclid(1, 122)
        for x in row:
            print(x.y == gcd(1, 122))
            print(x.y)
            print((row.t * row._b) % row._a)
