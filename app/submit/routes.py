from flask import render_template, redirect, url_for, session, request

from app import db
from app.submit import bp
from app import redis


@bp.route('/start', methods=['GET', 'POST'])
def start():
    return render_template('submit/start.html', title='Submit a Fast Stream role')


@bp.route('/role-details', methods=['GET', 'POST'])
def role_details():
    question = {'textarea': {'label': 'Role description',
                             'hint': "Please give a description of the role and some context. For example, what "
                                     "are the team's priorities?"},
                'text_input': {'for': 'role_title',
                               'label': 'Role title',
                               'hint': "This should be one of the 37 "
                                       "<a href='https://www.gov.uk/government/collections/digital-data-and-technology-profession-capability-framework'> "
                                       "DDaT roles"
                               },
                'radio': {'heading': 'What level of security clearance is required?',
                          'name': 'security-clearance-required',
                          'values': {'Baseline Personnel Security Standard': 'BPSS',
                                     'Security Check': 'SC',
                                     'Counter-Terrorism Check': 'CTC',
                                     'Developed Vetting': 'DV',
                                     'Not applicable': 'NA'}
                          }
                }
    if request.method == 'POST':
        print(request.form)
        print(request.form['email'])
        session[1] = request.form
    return render_template('submit/role-details.html', title='Role details', question=question)


@bp.route('/confirm-role-details', methods=['GET', 'POST'])
def confirm_role_details():
    data = request.form
    return render_template('submit/confirm-role-details.html', data=data)
