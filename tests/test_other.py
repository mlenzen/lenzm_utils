
from lenzm_utils.other import (
	valid_email_address,
	)


def test_valid_email_address():
	assert not valid_email_address('')
	assert not valid_email_address('a')
	assert not valid_email_address('(Hard Bounce)')
	assert not valid_email_address('@gmail.com')
	assert not valid_email_address('a@b')
	assert not valid_email_address('bob@localhost')
	assert valid_email_address('you@example.com')
