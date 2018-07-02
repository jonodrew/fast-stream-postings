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
                                     "are the team's priorities?",
                             'for': 'role-description'},
                'text_input': {'for': 'role-title',
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
                                     'Not applicable': 'NA'},
                          'for': 'clearance'
                          },
                'responsibilities': {'for': 'responsibilities',
                                     'label': 'Main responsibilities and deliverables of post',
                                     'hint': "We'll use this to decide if the role has sufficient stretch"}
                }
    if request.method == 'POST':
        print(request.form)
        print(request.form['email'])
        redis.set('role details', request.form)
    return render_template('submit/role-details.html', title='Role details', question=question)


@bp.route('/confirm-role-details', methods=['GET', 'POST'])
def confirm_role_details():
    data = redis.get('role details')
    return render_template('submit/confirm-role-details.html', data=data)
