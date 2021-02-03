from dotenv import load_dotenv
from os import getcwd, listdir


def create_environment():
    if ".env" in listdir(getcwd()):
        load_dotenv()
        load_dotenv(verbose=True)
        env_path = getcwd() + "/.env"
        load_dotenv(dotenv_path=env_path)
