import flask
import flask_sqlalchemy
import pytest

from lenzm_utils.flask import url_for_obj

app = flask.Flask(__name__)
app.config.update({
	'SERVER_NAME': 'localhost',
	'TESTING': True,
	'DEBUG': True,
	})
db = flask_sqlalchemy.SQLAlchemy(app)
blueprint = flask.Blueprint('blueprint', __name__)
app.register_blueprint(blueprint)


class Employee(db.Model):

	id = db.Column(db.Integer, primary_key=True)


class Manager(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String)
	last_name = db.Column(db.String)


@url_for_obj.register(Employee)
@blueprint.route('/employee/<int:id>')
def employee_view(id):
	pass


@url_for_obj.register(Manager, get_funcs={
	'full_name': lambda manager: manager.first_name + '_' + manager.last_name,
	})
@blueprint.route('/manager/<full_name>')
def manager_view(full_name):
	pass


def test_simple():
	employee = Employee(id=1)
	with app.app_context():
		# have to do this in a blueprint context for now
		# TODO this doesn't work - the code in the view doesn't get executed
		@blueprint.route('/testing')
		def test_view():
			assert url_for_obj.url_for_obj(employee) == flask.url_for('blueprint.employee_view', id=1)


def test_mapped():
	manager = Manager(first_name='M', last_name='Lenzen')
	with app.app_context():
		# have to do this in a blueprint context for now
		# TODO this doesn't work - the code in the view doesn't get executed
		@blueprint.route('/testing')
		def test_view():
			assert url_for_obj.url_for_obj(manager) == flask.url_for('blueprint.manager_view', full_name='M_Lenzen')
