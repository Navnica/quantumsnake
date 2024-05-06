class Session:
    def __init__(self, user: dict, role: dict) -> None:
        self.User.username = user['username']
        self.User.identification = user['identification']

        self.Role.name = role['name']
        self.Role.power_level = role['power_level']

    class User:
        username: str
        identification: int

    class Role:
        name: str
        power_level: int
