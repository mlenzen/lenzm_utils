from decimal import Decimal

from lenzm_utils import parse_string


def test_money():
	assert parse_string.money('') == Decimal(0)
	assert parse_string.money('1') == Decimal(1)
	assert parse_string.money('1,000') == Decimal(1000)
	assert parse_string.money('$1,000 ') == Decimal(1000)


def test_accounting():
	assert parse_string.accounting('') == Decimal(0)
	assert parse_string.accounting('-') == Decimal(0)
	assert parse_string.accounting('(1000)') == Decimal(-1000)


def test_percent_to_float():
	assert parse_string.percent_to_float('50%') == 0.5


def test_percent_to_decimal():
	assert parse_string.percent_to_decimal('50%') == Decimal('0.5')
