# -*- coding: utf-8 -*-
"""
Flask_LenzM_Utils
~~~~~~~~~~~~~~~~~~~

Utils for Flask Projects

:copyright: (c) 2016 by Michael Lenzen
:licence: MIT, see LICENCE for more details
"""
from flask import abort
from sqlalchemy import (
	Column,
	Integer,
	String,
	ForeignKey,
	)
from sqlalchemy.orm.exc import NoResultFound

from . import flask_db_admin, url_for_obj, url_update


def parent_key(column, col_type=Integer, nullable=False, index=True, **kwargs):
	return Column(
		col_type,
		ForeignKey(column, ondelete='CASCADE', onupdate='CASCADE'),
		nullable=nullable,
		index=index,
		**kwargs
		)


class BaseMixin():
	@classmethod
	def find_one(cls, **kwargs):
		return cls.query.filter_by(**kwargs).one()

	@classmethod
	def find_one_or_404(cls, **kwargs):
		try:
			cls.find_one(**kwargs)
		except NoResultFound:
			abort(404)

	@classmethod
	def find_create(cls, **kwargs):
		try:
			return cls.find_one(**kwargs)
		except NoResultFound:
			obj = cls(**kwargs)
			cls.query.session.add(obj)
			return obj

	@classmethod
	def exists(cls, **kwargs):
		try:
			cls.find_one(**kwargs)
			return True
		except NoResultFound:
			return False

	@classmethod
	def _repr_class_template(cls):
		col_names = [col.name for col in cls.__table__.columns]
		item_format = '{col}={{obj.{col}!r}}'
		fields = ', '.join(item_format.format(col=col) for col in col_names)
		return '{class_name}({fields})'.format(
			class_name=cls.__name__,
			fields=fields,
			)

	def __repr__(self):
		class_template = self._repr_class_template()
		return class_template.format(obj=self)

	@classmethod
	def pkey(cls, **kwargs):
		"""Return a column definition for the primary key of this model."""
		raise NotImplementedError

	@classmethod
	def fkey_constraint(cls, sport_abbr, team_abbr):
		"""Return a ForeignKeyConstraint for the primary keys of this model."""
		raise NotImplementedError


class IntegerPKey():

	id = Column(Integer, primary_key=True)

	@classmethod
	def pkey(cls, **kwargs):
		return parent_key(cls.id, Integer, **kwargs)
