from datetime import datetime, date

import pytest

from lenzm_utils.dates import (
	workday_diff,
	week_start,
	parse_date_missing_zero_padding,
	Month,
	week_start,
	past_complete_weeks,
	MON,
	)


d1 = datetime(2014, 7, 15, 12, 15)


HOLIDAYS = set((
	date(2013, 1, 1),  # New Year's Day
	date(2013, 1, 21),  # Martin Luther King, Jr. Day
	date(2013, 5, 27),  # Memorial Day
	date(2013, 7, 4),  # Independence Day
	date(2013, 7, 5),  # Recognition of Independence Day
	date(2013, 9, 2),  # Labor Day
	date(2013, 11, 28),  # Thanksgiving
	date(2013, 11, 29),  # Friday after Thanksgiving
	date(2013, 12, 24),  # Christmas Eve
	date(2013, 12, 25),  # Christmas Day
	date(2013, 12, 26),  # Day after Christmas
	date(2013, 12, 31),  # New Year's Eve
	date(2014, 1, 1),  # New Year's Day
	date(2014, 1, 20),  # Martin Luther King, Jr. Day
	date(2014, 2, 17),  # President's Day
	date(2014, 5, 26),  # Memorial Day
	date(2014, 7, 3),  # Recognition of Independence Day
	date(2014, 7, 4),  # Independence Day
	date(2014, 9, 1),  # Labor Day
	date(2014, 11, 27),  # Thanksgiving
	date(2014, 11, 28),  # Friday after Thanksgiving
	date(2014, 12, 24),  # Christmas Eve
	date(2014, 12, 25),  # Christmas Day
	date(2014, 12, 26),  # Day after Christmas
	date(2014, 12, 31),  # New Year's Eve
	date(2015, 1, 1),  # New Year's Day
	date(2015, 1, 19),  # Martin Luther King, Jr. Day
	date(2015, 2, 16),  # President's Day
	date(2015, 5, 25),  # Memorial Day
	date(2015, 7, 2),  # Recognition of Independence Day
	date(2015, 7, 3),  # Recognition of Independence Day (Federal Holiday)
	date(2015, 9, 7),  # Labor Day
	date(2015, 11, 26),  # Thanksgiving
	date(2015, 11, 27),  # Day after Thanksgiving
	date(2015, 12, 24),  # Christmas Eve
	date(2015, 12, 25),  # Christmas Day
	date(2015, 12, 31),  # New Year's Eve
	date(2016, 1, 1),  # New Year's Day
	date(2016, 1, 18),  # Martin Luther King, Jr. Day
	date(2016, 2, 15),  # President's Day
	date(2016, 5, 30),  # Memorial Day
	date(2016, 7, 1),  # Recognition of Independence Day
	date(2016, 7, 4),  # Independence Day
	date(2016, 9, 5),  # Labor Day
	date(2016, 11, 24),  # Thanksgiving
	date(2016, 11, 25),  # Day after Thanksgiving
	date(2016, 12, 23),  # Recognition of Christmas Eve
	date(2016, 12, 26),  # Christmas Day (Federal Observed)
	date(2016, 12, 30),  # Recognition of New Year's Eve
	date(2017, 1, 2),  # New Year's Day (Federal Observed)
	))


class TestWorkdayDiff:

	def test_one_day(self):
		d2 = datetime(2014, 7, 16, 12, 15)
		assert workday_diff(d1, d2, holidays=HOLIDAYS) == 1
		assert workday_diff(d2, d1, holidays=HOLIDAYS) == -1

	def test_full_year(self):
		d2 = datetime(2013, 7, 15, 12, 15)
		assert workday_diff(d2, d1, holidays=HOLIDAYS) == 365 - (52 * 2) - 13
		assert workday_diff(d1, d2, holidays=HOLIDAYS) == -(365 - (52 * 2) - 13)

	def test_partial_day(self):
		d2 = datetime(2014, 7, 15, 18, 15)
		assert workday_diff(d1, d2, holidays=HOLIDAYS) == 0.25
		assert workday_diff(d2, d1, holidays=HOLIDAYS) == -0.25

	def test_concurrent_partial_days(self):
		d2 = datetime(2014, 7, 16, 18, 15)
		assert workday_diff(d1, d2, holidays=HOLIDAYS) == 1.25
		assert workday_diff(d2, d1, holidays=HOLIDAYS) == -1.25

	def test_weekend(self):
		d2 = datetime(2014, 7, 23, 18, 15)
		assert workday_diff(d1, d2, holidays=HOLIDAYS) == 6.25
		assert workday_diff(d2, d1, holidays=HOLIDAYS) == -6.25

	def test_holidays_and_weekend(self):
		d2 = datetime(2014, 7, 2, 6, 15)
		assert workday_diff(d2, d1, holidays=HOLIDAYS) == 7.25
		assert workday_diff(d1, d2, holidays=HOLIDAYS) == -7.25


class TestWeekStart:

	def test_sunday(self):
		assert week_start(datetime(2014, 10, 12, 0, 0, 0)) == date(2014, 10, 12)

	def test_monday(self):
		assert week_start(datetime(2014, 10, 13, 1, 1, 1)) == date(2014, 10, 12)

	def test_tuesday(self):
		assert week_start(datetime(2014, 10, 14, 1, 1, 1)) == date(2014, 10, 12)

	def test_wednesday(self):
		assert week_start(datetime(2014, 10, 15, 1, 1, 1)) == date(2014, 10, 12)

	def test_thursday(self):
		assert week_start(datetime(2014, 10, 16, 1, 1, 1)) == date(2014, 10, 12)

	def test_friday(self):
		assert week_start(datetime(2014, 10, 17, 1, 1, 1)) == date(2014, 10, 12)

	def test_saturday(self):
		assert week_start(datetime(2014, 10, 18, 23, 59, 59)) == date(2014, 10, 12)


class TestWeekStartMon:

	def test_sunday(self):
		assert week_start(datetime(2014, 10, 12, 0, 0, 0), MON) == date(2014, 10, 6)

	def test_monday(self):
		assert week_start(datetime(2014, 10, 13, 1, 1, 1), MON) == date(2014, 10, 13)

	def test_tuesday(self):
		assert week_start(datetime(2014, 10, 14, 1, 1, 1), MON) == date(2014, 10, 13)

	def test_wednesday(self):
		assert week_start(datetime(2014, 10, 15, 1, 1, 1), MON) == date(2014, 10, 13)

	def test_thursday(self):
		assert week_start(datetime(2014, 10, 16, 1, 1, 1), MON) == date(2014, 10, 13)

	def test_friday(self):
		assert week_start(datetime(2014, 10, 17, 1, 1, 1), MON) == date(2014, 10, 13)

	def test_saturday(self):
		assert week_start(datetime(2014, 10, 18, 23, 59, 59), MON) == date(2014, 10, 13)


class Test_parse_date_missing_zero_padding:

	def test_simple(self):
		assert parse_date_missing_zero_padding('3/1/15') == date(2015, 3, 1)

	def test_order(self):
		assert parse_date_missing_zero_padding('1/15/3', order='dym') == date(2015, 3, 1)

	def test_min_year1(self):
		assert parse_date_missing_zero_padding('3/1/15', min_year=1900) == date(1915, 3, 1)

	def test_min_year2(self):
		assert parse_date_missing_zero_padding('3/1/15', min_year=1950) == date(2015, 3, 1)

	def test_full_year(self):
		assert parse_date_missing_zero_padding('3/1/2015') == date(2015, 3, 1)

	def test_100_year(self):
		assert parse_date_missing_zero_padding('3/1/100', min_year=0) == date(100, 3, 1)

	def test_invalid_years(self):
		with pytest.raises(ValueError):
			parse_date_missing_zero_padding('3/1/100')
		with pytest.raises(ValueError):
			parse_date_missing_zero_padding('3/1/-1')

	def test_missing_values(self):
		with pytest.raises(ValueError):
			parse_date_missing_zero_padding('3/1')


def test_Month_first():
	assert Month(2012, 5).first() == date(2012, 5, 1)


def test_Month_mid():
	assert Month(2012, 5).mid() == date(2012, 5, 15)


def test_Month_next():
	assert Month(2012, 5).next() == Month(2012, 6)
	assert Month(2012, 12).next() == Month(2013, 1)


def test_Month_from_date():
	assert Month.from_date(date(2012, 5, 12)) == Month(2012, 5)


def test_Month_lt():
	assert Month(2012, 5) < Month(2012, 6)
	assert Month(2012, 5) < Month(2013, 4)
	assert Month(2012, 12) < Month(2013, 1)
	assert not Month(2012, 5) < Month(2012, 5)
	assert not Month(2012, 5) < Month(2012, 4)
	assert not Month(2012, 5) < Month(2011, 6)


def test_Month_sub():
	assert Month(2012, 5) - Month(2012, 5) == 0
	assert Month(2012, 5) - Month(2012, 4) == 1
	assert Month(2012, 5) - Month(2011, 5) == 12
	assert Month(2012, 4) - Month(2012, 5) == -1
	assert Month(2011, 5) - Month(2012, 5) == -12


def test_Month_date():
	m = Month(2012, 5)
	assert m.date(1) == date(2012, 5, 1)
	assert m.date(31) == date(2012, 5, 31)
	assert m.date(-1) == date(2012, 5, 31)
	with pytest.raises(ValueError):
		m.date(-32)
	with pytest.raises(ValueError):
		m.date(0)


def test_week_start():
	assert week_start(date(2015, 6, 25)) == date(2015, 6, 21)
	assert week_start(date(2015, 6, 21)) == date(2015, 6, 21)
	assert week_start(date(2015, 6, 27)) == date(2015, 6, 21)


def test_past_complete_weeks():
	today = date(2016, 2, 9)
	assert past_complete_weeks(1, today) == (date(2016, 1, 31), date(2016, 2, 7))
