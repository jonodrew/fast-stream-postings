from typing import Dict, List
import json


class RoleQuestion:
    def __init__(self, name: str, skills: Dict[str, str]):
        self.name = name
        self.skills = skills


class Family:
    def __init__(self, name: str, roles: List[RoleQuestion]):
        self.name = name
        self.roles = roles


def skill_dump(form) -> str:
    skills = {
        'Skills gained': ' | '.join(form.getlist('skills')),
        'Overall level attained': form.get('skill-level'),
        'How gained': form.get('skills-describe')
    }
    return json.dumps(skills)
