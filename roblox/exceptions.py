

class InvalidAccount(Exception):
    pass


class AnUnknownError(Exception):
    pass


class BannedAccount(Exception):
    pass


class CookieNotFound(Exception):
    pass


class CaptchaTimeout(Exception):
    pass
