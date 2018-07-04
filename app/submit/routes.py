from flask import render_template, redirect, url_for, session, request
from app.submit.classes import RoleQuestion
from app import db
from app.submit import bp
from app import redis


@bp.route('/start', methods=['GET', 'POST'])
def start():
    return render_template('submit/start.html', title='Submit a Fast Stream role')


@bp.route('/role-details', methods=['GET', 'POST'])
def role_details():
    if request.method == 'POST':
        redis.set('role details', request.form)
        return redirect(url_for('submit.role_family'))
    question = {
        'textarea': {
            'label': 'Role description',
                             'hint': "Please give a description of the role and some context. For example, what "
                                     "are the team's priorities?",
                             'for': 'role-description'
        },
        'role_title': {
            'for': 'role-title',
            'label': 'Role title',
            'hint': "For preference, this should be one of the 37 "
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


@bp.route('/role-family', methods=['POST', 'GET'])
def role_family():
    if request.method == 'POST':
        roles = {
                'data': {
                    'data-engineer': 'Data engineer',
                    'Data scientist': 'data_scientist',
                    'Performance analyst': 'performance_analyst'
                }
            }
        redis.set('family', request.form['ddat-job-family'])
        family = request.form['ddat-job-family']
        return redirect(url_for('submit.skills'))
    question = {
        'family': {
            'heading': 'In which job family does this role sit?',
            'name': 'ddat-job-family',
            'values': {'Data': 'data',
                      'IT Operations': 'ITOps',
                      'Product and delivery': 'PD',
                      'Quality Assurance Testing': 'QAT',
                      'Technical': 'technical',
                      'User-centred design': 'UCD'},
            'for': 'ddat_job_family'
        }
    }
    redis.set('roles_seen', 0)
    return render_template('submit/role-family.html', question=question)


@bp.route('/skills', methods=['POST', 'GET'])
def skills():
    r = RoleQuestion('Data Engineer', {
                            'Data analysis and synthesis': 1031,
                            'Communicating between the technical and the non-technical': 1023,
                            'Data development process': 1033,
                            'Data integration design': 1037,
                            'Data modelling': 1038,
                            'Programming and build (data engineering)': 1084,
                            'Technical understanding (data engineering)': 1116,
                            'Testing': 1118
                        })
    r2 = RoleQuestion('Data Engineer Mk 2', {
                            'Data analysis and synthesis': 1031,
                            'Communicating between the technical and the non-technical': 1023,
                            'Data development process': 1033,
                            'Data integration design': 1037,
                            'Data modelling': 1038,
                            'Programming and build (data engineering)': 1084,
                            'Technical understanding (data engineering)': 1116,
                            'Testing': 1118
                        })
    r3 = RoleQuestion('Strategy and Policy', {
                            'Drafting': 1,
                            'Briefing': 2,
                            'Research': 3,
                            'Working with ministers': 4,
                            'Bills and legislation': 5,
                            'Policy evaluation': 6,
                            'Parliamentary questions/Freedom of Information requests': 7
                         })
    r4 = RoleQuestion('Generalist skill areas', {
                            'Commercial awareness': 11,
                            'Financial management': 12,
                            'People management': 13,
                            'Programme management': 14,
                            'Change management': 15,
                            'Science/engineering policy facing': 16,
                            'International policy facing': 17

                        })
    families = {
        'data': [r, r2, r3, r4]
        }
    roles_in_family = families[redis.get('family')]
    next_step = 'submit.skills'
    if request.method == 'POST':  # user has clicked 'complete'
        redis.incr('roles_seen', 1)  # increment the number of roles seen
        seen_roles = int(redis.get('roles_seen'))
        if request.form:
            redis.hmset('skills-{}'.format(seen_roles-1), request.form)
        if seen_roles == len(roles_in_family) - 1:
            next_step = 'submit.logistical_details'
    seen_roles = int(redis.get('roles_seen'))
    current_role = roles_in_family[seen_roles]
    r = {
        'title': current_role.name,
        'skills': {
            'heading': 'Which of the following skills will this role develop?',
            'name': '{}-skills'.format(current_role.name),
            'values': current_role.skills,
            'for': '{}-skills'.format(current_role.name)
        }
    }
    return render_template('submit/skills.html', role=r, next_step=next_step)


@bp.route('/logistical-details', methods=['POST', 'GET'])
def logistical_details():
    if request.method == 'POST':
        redis.set('role specifics', request.form)
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
                         'hint': "We'll email a copy of this completed form to that address"},
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
