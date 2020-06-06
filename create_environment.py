from dotenv import load_dotenv
from os import getcwd

load_dotenv()
load_dotenv(verbose=True)
env_path = getcwd() + "/.env"
print(env_path)
load_dotenv(dotenv_path=env_path)
