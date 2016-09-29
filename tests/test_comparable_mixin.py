import itertools

import pytest

from lenzm_utils.comparable_mixin import ComparableIsInstanceMixin


class CompWrap(ComparableIsInstanceMixin):
	def __init__(self, i):
		self.i = i

	def _cmp_key(self):
		return self.i


OBJS = [-2, -1, 0, 1, 2]

def lt(a, b): return a < b
def le(a, b): return a <= b
def gt(a, b): return a > b
def ge(a, b): return a >= b
def eq(a, b): return a == b
def ne(a, b): return a != b
def ha(a, b): return hash(a) == hash(b)

OPERANDS = [lt, le, gt, ge, eq, ne, ha]


@pytest.mark.parametrize('i', OBJS)
def test_hash(i):
	assert hash(i) == hash(CompWrap(i))


@pytest.mark.parametrize('i, j, operand', itertools.product(OBJS, OBJS, OPERANDS))
def test_comparable_mixin(i, j, operand):
	assert operand(CompWrap(i), CompWrap(j)) == operand(i, j)
