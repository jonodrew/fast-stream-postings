from flask import render_template, redirect, url_for, session, request
from app.submit.classes import RoleQuestion
from app import db
from app.submit import bp
from app import redis
from redis import ResponseError


@bp.route('/start', methods=['GET', 'POST'])
def start():
    redis.flushall()
    return render_template('submit/start.html', title='Submit a Fast Stream role')


@bp.route('/role-details', methods=['GET', 'POST'])
def role_details():
    if request.method == 'POST':
        details = request.form.to_dict()
        redis.hmset('role', details)
        return redirect(url_for('submit.role_family'))
    question = {
        'textarea': {
            'label': 'Role description',
                             'hint': "Please give a description of the role and some context. For example, what "
                                     "are the team's priorities?",
                             'for': 'Description'
        },
        'role_title': {
            'for': 'Title',
            'label': 'Role title',
            'hint': "For preference, this should be one of the 37 "
                    "<a href='https://www.gov.uk/government/collections/digital-data-and-technology-profession-capability-framework'> "
                    "DDaT roles"
                       },
                'responsibilities': {'for': 'Key responsibilities',
                                     'label': 'Main responsibilities and deliverables of post',
                                     'hint': "We'll use this to decide if the role has sufficient stretch"}
                }
    return render_template('submit/role-details.html', title='Role details', question=question)


@bp.route('/role-family', methods=['POST', 'GET'])
def role_family():
    if request.method == 'POST':
        redis.set('family', request.form['ddat-job-family'])
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
            'for': 'DDaT job family'
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
        seen_roles = int(redis.get('roles_seen'))
        rq = request.form
        # request passes checked boxes as list!!!
        redis.hmset('skills{}'.format(seen_roles), rq)
        raise
        redis.incr('roles_seen', 1)  # increment the number of roles seen
        print(request.form.to_dict())
        if seen_roles == len(roles_in_family) - 1:
            next_step = 'submit.logistical_details'
    seen_roles = int(redis.get('roles_seen'))
    current_role = roles_in_family[seen_roles]
    name = current_role.name.replace(' ', '-').lower()
    r = {
        'title': name,
        'skills': {
            'heading': 'Which of the following skills will this role develop?',
            'name': '{}-skills'.format(name),
            'values': current_role.skills,
            'for': '{}-skills'.format(name)
        },
        'description': {
                'label': 'How will the role deliver these skills?',
                'hint': "Please give a brief description of how this role will develop the Fast Streamers skills in the"
                        " areas you've indicated. If you've not ticked anything, there's no need to complete this box.",
                'for': '{}-skills-describe'.format(name)
        },
        'skill_level': {
            'heading': 'What level of skill will the candidate gain?',
            'name': '{}-skill-level'.format(name),
            'values': {
                'Awareness': 1,
                'Working': 2,
                'Practitioner': 3,
                'Expert': 4
            },
            'for': '{}-skill-level'.format(name),
            'hint': "Across all the skills you've indicated, what level of ability do you expect the Fast Streamer to "
                    "have at the end of this post?"
        }
    }
    return render_template('submit/skills.html', role=r, next_step=next_step)


@bp.route('/logistical-details', methods=['POST', 'GET'])
def logistical_details():
    if request.method == 'POST':
        redis.hmset('generalist_skills', request.form.to_dict())
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
                'experience': {
                    'heading': 'How much experience do you expect the Fast Streamer to aleady have to be efficient in '
                               'this role?',
                               'name': 'post-length',
                               'values': {'0 - 6 months': 1,
                                          '12 - 18 months': 2,
                                          '2 years': 3,
                                          '3 years': 4
                                          },
                               'for': 'Experience required',
                    'hint': 'Remember that this is the amount of general DDaT experience, rather than experience in '
                            'this area'
                },
                'ongoing': {
                    'heading': 'Is this post a one-off, or ongoing?',
                    'name': 'ongoing',
                    'values': {
                        'One-off': 'one-off',
                        'Ongoing': 'ongoing'
                    },
                    'for': 'Ongoing or one-off?'
                },
                'start': {'for': 'Start month',
                          'label': 'What month would you prefer the Fast Streamer start?',
                          'hint': 'The start date will generally be 1st of the month, unless the Fast Streamer has'
                                  ' already booked some leave.'}

                }
    return render_template('submit/logistical-details.html', question=question)


@bp.route('security', methods=['POST', 'GET'])
def security():
    if request.method == 'POST':
        redis.hmset('logistics', request.form.to_dict())
    question = {
        'clearance': {
            'heading': 'What level of security clearance is required?',
            'name': 'security-clearance-required',
              'values': {'Baseline Personnel Security Standard': 'BPSS',
                         'Security Check': 'SC',
                         'Counter-Terrorism Check': 'CTC',
                         'Developed Vetting': 'DV',
                         'Not applicable': 'NA'},
              'for': 'clearance'
        },
        'nationality': {
            'for': 'nationality-restriction',
            'label': 'Are there any restrictions on the nationality of the Fast Streamer?',
            'hint': "For preference, this should be one of the 37 "
                    "<a href='https://www.gov.uk/government/collections/digital-data-and-technology-profession-capability-framework'> "
                    "DDaT roles"
        },
    }
    return render_template('submit/security.html', question=question)


@bp.route('/contact-details', methods=['GET', 'POST'])
def contact_details():
    if request.method == 'POST':
        redis.hmset('security', request.form.to_dict())
    question = {
        'am_email': {
            'for': 'activity-manager-email',
            'label': 'Please give the activity manager\'s email address',
            'hint': "We'll email a copy of this completed form to that address"
        },
        'location': {
            'for': 'activity-manager-location',
            'label': 'Please give an address for this role',
            'hint': 'Please include a postcode. We generally find that Activity Managers who are local '
                     'to their Fast Streamer get greater benefit. '
        },
        'grade': {
            'for': 'activity-manager-grade',
            'label': 'What grade will the Fast Streamer\'s Activity Manager hold?',
            'hint': 'In general we expect this to be a Grade 7 or equivalent for trainees with less than two years '
                    'experience, and a Grade 6 or equivalent for those with more'
        },
        'grade_manager': {
            'for': 'grade-manager-email',
            'label': 'Please give the grade manager\'s email address',
            'hint': "We'll email a copy of this completed form to that address"
        }
    }
    return render_template('submit/contact-details.html', question=question)


@bp.route('/confirm-role-details', methods=['GET', 'POST'])
def confirm_role_details():
    if request.method == 'POST':
        redis.hmset('contact', request.form.to_dict())
    data = {
        'role': {
            'caption': 'Role details',
            'row_data': redis.hgetall('role')
        },
        'logistics': {
            'caption': 'Logistical details',
            'row_data': redis.hgetall('logistics')
        },
        'security': {
            'caption': 'Security details',
            'row_data': redis.hgetall('security')
        }
    }
    number_of_roles = int(redis.get('roles_seen'))
    for i in range(number_of_roles):
        potential_key = 'skills{}'.format(i)
        skill_data = {
            'row_data': redis.hgetall(potential_key),
            'caption': potential_key
        }
        data[potential_key] = skill_data
    return render_template('submit/confirm-role-details.html', data=data)
