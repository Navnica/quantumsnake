class Session:
    identification: int
    username: str

    def __init__(self, identification: int, username: str) -> None:
        self.identification = identification
        self.username = username
