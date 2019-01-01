from flask import render_template, redirect, url_for, session, request, flash
from app.auth import bp


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authorised_login(username, password):
            session['user_id'] = 'authorised_user'
        else:
            return redirect(url_for('auth.login'))
        return redirect(url_for('submit.start'))
    questions = [
        {
            'username_question': {
                'for': 'username',
                'label': "Please enter the username you've been given",
                'hint': "If you don't have the username, please contact the service owner"
            }
        },
        {
            'password-question': {
                'for': 'password',
                'label': "Please enter the password you've been given",
                'hint': "If you don't have the password, please contact the service owner"
            }
        }
    ]
    return render_template('auth/login.html', questions=questions)


def authorised_login(user, password):
    return user == 'activity-manager' and password == "submit-my-role"
