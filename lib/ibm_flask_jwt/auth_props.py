from environs import Env


class AuthProps:

    def __init__(self):
        self._env = Env()
        self._env.read_env()

    def log_level(self):
        return self._env('LOG_LEVEL', 'INFO')

    def jwt_public_key(self):
        return self._env('JWT_PUBLIC_KEY')
