

class RobloxAccount:
    def __init__(self, username: str, password: str, cookie: str, robux: int):
        self._username = username
        self._password = password
        self._cookie = cookie
        self._robux = robux

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str) -> None:
        self._username = value

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: str) -> None:
        self._password = value

    @property
    def cookie(self) -> str:
        return self._cookie

    @cookie.setter
    def cookie(self, value: str) -> None:
        self._cookie = value

    @property
    def robux(self) -> int:
        return self._robux

    @robux.setter
    def robux(self, value: int) -> None:
        self._robux = value
