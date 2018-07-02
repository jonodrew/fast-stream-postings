from typing import List


class Role:
    def __init__(self, name: str, skills: List[str], level: str):
        self.name = name
        self.skills = skills
        self.level = level


class Family:
    def __init__(self, name: str, roles: List[Role]):
        self.name = name
        self.roles = roles
