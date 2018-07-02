from flask import render_template, redirect, url_for, session, request

from app import db
from app.submit import bp
from app import redis


@bp.route('/start', methods=['GET', 'POST'])
def start():
    redis.set('role data', {})
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
    return render_template('submit/role-details.html', title='Role details', question=question)


@bp.route('/logistical-details', methods=['POST', 'GET'])
def logistical_details():
    if request.method == 'POST':
        redis.set('role details', request.form)
    question = {'department': {'for': 'department',
                               'label': 'What department or agency is this role in?',
                               'hint': "What's your organisation generally known as?"},
                'directorate': {'for': 'directorate',
                                'label': 'Which business area or directorate is this role in?',
                                'hint': 'This should describe the immediate context in which the Fast Streamer will be'
                                        ' working.'},
                'location': {'for': 'location',
                             'label': 'Please give an address for this role',
                             'hint': 'Please include a postcode. This might not be where the Fast Streamer will spend'
                                     'all their time, but it will help us decide whether they\'ll need to relocate'},
                'length': {'heading': 'How long is this post?',
                           'name': 'post-length',
                           'values': {'6 months': 6,
                                      '12 months': 12},
                           'for': 'post-length'},
                'ongoing': {'heading': 'Is this post a one-off, or ongoing?',
                            'name': 'ongoing',
                            'values': {'One-off': 'one-off',
                                       'Ongoing': 'ongoing'},
                            },
                'start': {'for': 'start-month',
                          'label': 'What month would you prefer the Fast Streamer start?',
                          'hint': 'The start date will generally be 1st of the month, unless the Fast Streamer has'
                                  ' already booked some leave.'}

                }
    return render_template('submit/logistical-details.html', question=question)


@bp.route('/contact-details', methods=['GET', 'POST'])
def contact_details():
    if request.method == 'POST':
        redis.set('logistical details', request.form)
    question = {'name': {'for': 'activity-manager-name',
                         'label': 'Please give the activity manager\'s email address',
                         'hint': ''},
                'location': {'for': 'activity-manager-location',
                             'label': 'Please give an address for this role',
                             'hint': 'Please include a postcode. We generally find that Activity Managers who are local'
                                     'to their Fast Streamer get greater benefit. '},
                'grade': {'for': 'activity-manager-grade',
                          'label': 'What grade will the Fast Streamer\'s Activity Manager hold?',
                          'hint': 'In general we expect this to be a Grade 7 or equivalent for 6 month posts and a '
                                  'Grade 6 or equivalent for 12 month posts'}
                }
    return render_template('submit/contact-details.html', question=question)


@bp.route('/confirm-role-details', methods=['GET', 'POST'])
def confirm_role_details():
    data = {
        'role details': redis.get('role details'),
        'logistics': redis.get('logistical details'),
        'contact': request.form
    }
    return render_template('submit/confirm-role-details.html', data=data)
