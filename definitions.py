import os

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
DB_ENGINE_URL = "sqlite:///"+ROOT_DIR+"/sessions.db"
DB_CLIENT_ENCODING = "utf8"
COOKIE_NAME = "chess-session"
ARGUMENT_INJECTION_PERCENTAGE_THRESHOLD = 0.9
TOTAL_NR_OF_INJECTIONS_THRESHOLD = 10