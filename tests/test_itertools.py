from collections import OrderedDict

import pytest

from lenzm_utils.itertools import (
	product,
	all_equal,
	one,
	first,
	last,
	nth,
	count,
	)


def test_product():
	assert product((1, 2, 3)) == 6


def test_nth():
	assert nth(set('a'), 0) == 'a'
	od = OrderedDict()
	od['a'] = 1
	od['b'] = 2
	od['c'] = 3
	assert nth(od, 0) == 'a'
	assert nth(od, 1) == 'b'
	assert nth(od, 2) == 'c'
	with pytest.raises(ValueError):
		nth(od, 3)
	assert nth(od, -1) == 'c'
	assert nth(od, -2) == 'b'
	assert nth(od, -3) == 'a'
	with pytest.raises(ValueError):
		nth(od, -4)


def test_all_eq():
	assert all_equal((0.0, 0, 1 - 1))
	assert all_equal(('a', 'a'))
	assert all_equal((1, ))
	assert all_equal([])
	assert not all_equal((1, 2, 3))
	assert not all_equal((1, 1, 2))


def test_first():
	assert first('abc') == 'a'
	with pytest.raises(ValueError):
		first('')
	assert first(set('abc')) in 'abc'
	assert first((0.0, 0, 0)) == 0.0


def test_one():
	assert one('a') == 'a'
	assert one(range(1)) == 0
	assert one(set('c')) == 'c'
	with pytest.raises(ValueError):
		one([])
	with pytest.raises(ValueError):
		one('ab')
