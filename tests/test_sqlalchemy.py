from datetime import datetime

import pytz
import pytest
from sqlalchemy import create_engine, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.orm as orm

from lenzm_utils.sqlalchemy import CIText, UTCDateTime

Base = declarative_base()


@pytest.fixture(scope='session')
def session(request):
	engine = create_engine('postgresql://test:test@localhost/test')
	conn = engine.connect()
	Base.metadata.bind = conn
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)
	# meta.drop_all()
	# meta.create_all()

	transaction = conn.begin()
	Session = orm.sessionmaker(bind=conn)
	sess = Session()

	def teardown():
		transaction.rollback()
		Base.metadata.drop_all(engine)
		conn.close()
		# sess.remove()

	request.addfinalizer(teardown)
	return sess


class CIKeyObj(Base):

	__tablename__ = 'ci_key_obj'

	id = Column(CIText, primary_key=True)

	def __repr__(self):
		return f"CIKeyObj({self.id})"


class UTCDateTimeTestObj(Base):

	__tablename__ = 'utc_datetime_obj'

	id = Column(Integer, primary_key=True)
	ts = Column(UTCDateTime)


def test_citext(session):
	to = CIKeyObj(id='FooFighter')
	session.add(to)
	session.commit()
	row = session.query(CIKeyObj).filter(CIKeyObj.id == 'foofighter').all()
	assert len(row) == 1
	print(row)
	assert session.query(CIKeyObj).get('fOOfIGHTER')
	session.close()


def test_utc_datetime(session):
	now = datetime.now().replace(tzinfo=pytz.timezone('America/Chicago'))
	obj = UTCDateTimeTestObj(ts=now)
	session.add(obj)
	session.commit()
	obj = session.query(UTCDateTimeTestObj).one()
	assert obj.ts.tzinfo == pytz.utc
	session.add(UTCDateTimeTestObj(ts=datetime.now()))
	with pytest.raises(ValueError):
		session.flush()


def test_parse_uuid():
	pass
	# TODO write parse uuid test
