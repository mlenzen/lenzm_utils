import pytest
from sqlalchemy import create_engine, MetaData, Integer
from sqlalchemy.schema import Column, Table
import sqlalchemy.orm as orm

from lenzm_utils.sqlalchemy import CIText


@pytest.fixture(scope='session')
def session(request):
	engine = create_engine('postgresql://test:test@localhost/test')
	conn = engine.connect()
	meta.bind = conn
	meta.drop_all()
	meta.create_all()

	transaction = conn.begin()
	Session = orm.sessionmaker(bind=conn)
	sess = Session()

	def teardown():
		transaction.rollback()
		meta.drop_all()
		conn.close()
		# sess.remove()

	request.addfinalizer(teardown)
	return sess


meta = MetaData()

test_table = Table(
	'test',
	meta,
	Column('id', Integer(), primary_key=True),
	Column('txt', CIText()),
	)


class CIKeyObj(object):

	def __init__(self, id_, txt):
		self.id = id_
		self.txt = txt

	def __repr__(self):
		return "TestObj(%r, %r)" % (self.id, self.txt)


orm.mapper(CIKeyObj, test_table)


def test_citext(session):
	to = CIKeyObj(1, txt='FooFighter')
	session.add(to)
	session.commit()
	row = session.query(CIKeyObj).filter(CIKeyObj.txt == 'foofighter').all()
	assert len(row) == 1
	print(row)
	session.close()
