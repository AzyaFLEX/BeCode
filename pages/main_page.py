from flask_login import login_user, logout_user, current_user, LoginManager, login_required
from classes.courses import Courses
from classes.lesson import Lesson
import flask_login
import flask

from data import db_session

blueprint = flask.Blueprint(
    'main_page',
    __name__,
    template_folder='templates',
    static_folder="static"
)


@blueprint.route('/')
def main_page():
    return flask.render_template("main.html", title='BeCode', postfix='', user=current_user)


@blueprint.route('/courses', methods=['GET'])
@blueprint.route('/courses/', methods=['GET'])
@login_required
def courses():
    return flask.render_template("courses.html", title='BeCode: Courses', postfix='Courses', user=current_user, courses=Courses())


@blueprint.route('/courses/<string:name>', methods=['GET'])
@login_required
def lesson(name: str):
    return flask.render_template("main_course_page.html", title=f'BeCode: {name.capitalize()}',
                                 postfix=name.capitalize(), user=current_user, topic=Lesson(name.lower()))
