import pathlib


class Sqlite:

    def __init__(
        self,
        sqlite_path: pathlib.Path,
    ):
        self.sqlite_path = sqlite_path

