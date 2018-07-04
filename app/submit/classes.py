from typing import Dict, List


class RoleQuestion:
    def __init__(self, name: str, skills: Dict[str, int]):
        self.name = name
        self.skills = skills


class Family:
    def __init__(self, name: str, roles: List[RoleQuestion]):
        self.name = name
        self.roles = roles
