class Session:
    def __init__(self, user: dict, role: dict, video_files: list) -> None:
        self.User.username = user['username']
        self.User.identification = user['identification']

        self.Role.name = role['name']
        self.Role.power_level = role['power_level']
        self.Role.access_code = role['access_code']

        self.VideoFiles.files = video_files

    class User:
        username: str
        identification: int

    class Role:
        name: str
        power_level: int
        access_code: str

    @staticmethod
    class VideoFiles:
        files: list

        def add_file(self, file) -> None:
            self.files.append(file)

        def get_all(self) -> list:
            return self.files

        def find_by_name(self, name):
            for file in self.files:
                if file.name == name:
                    return file

            raise KeyError

        class VideoFile:
            name: str
            tag: str

            def __init__(self, name: str, tag: str) -> None:
                self.name = name
                self.tag = tag
