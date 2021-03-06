from flask_login import login_user, logout_user, current_user, LoginManager, login_required, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from form.registration import RegistrationForm
from werkzeug.utils import redirect
from form.login import LoginForm
from classes.user import User
from data import db_session
from main import load_user
import sqlite3
import flask


blueprint = flask.Blueprint(
    'sign',
    __name__,
    template_folder='templates'
)


@blueprint.route('/registration', methods=['GET', 'POST'])
@blueprint.route('/registration/', methods=['GET', 'POST'])
def register():
    if not isinstance(current_user._get_current_object(), AnonymousUserMixin):
        return redirect('/')
    form = RegistrationForm()
    if form.validate_on_submit():
        con = sqlite3.connect('db/courses.db')
        cur = con.cursor()
        if form.username.data in map(lambda x: x[0], cur.execute('''SELECT login FROM users''').fetchall()):
            return flask.render_template('signup.html', title='BeCode: SignUp',
                                         postfix='Registration', form=form, user=current_user, error_ex='Login already exist')
        elif form.email.data in map(lambda x: x[0], cur.execute('''SELECT email FROM users''').fetchall()):
            return flask.render_template('signup.html', title='BeCode: SignUp',
                                         postfix='Registration', form=form, user=current_user, error_ex='Email already exist')
        session = db_session.create_session()
        user = User()
        user.login, user.hashed_password, user.email = [form.username.data, generate_password_hash(form.password.data.lower()),
                                                        form.email.data]
        session.add(user)
        session.commit()
        login_user(user)
        print(f'{form.username.data} successful signed in')
        return redirect('/courses')
    return flask.render_template('signup.html', title='BeCode: SignUp',
                                 postfix='Registration', form=form, user=current_user, error_ex='')


@blueprint.route('/login', methods=['GET', 'POST'])
@blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    # if current_user:
    #     return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.login == form.username.data).first()
        if user is None:
            return flask.render_template('signin.html', title='BeCode: SignIn', postfix='Login',
                                         form=form, exception='Wrong login', user=current_user)
        if check_password_hash(user.hashed_password, form.password.data.lower()):
            login_user(user, remember=form.remember_me.data)
            return redirect("/courses")
        return flask.render_template('signin.html', title='BeCode: SignIn', postfix='Login', form=form,
                                     exception='Wrong password', user=current_user)
    return flask.render_template('signin.html', title='BeCode: SignIn',
                                 postfix='Login', form=form, user=current_user)


@blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@blueprint.route('/test/user/<int:user_id>', methods=['GET'])
def get_user_id(user_id):
    db_sess = db_session.create_session()
    data = db_sess.query(User).get(user_id)
    if data:
        return flask.jsonify({'user': data.to_dict()})
    return flask.jsonify({'error': 'missed id'})
