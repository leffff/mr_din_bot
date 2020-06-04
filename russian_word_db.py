from os import getcwd, mkdir
import requests


def directory_creator():
    path = getcwd() + "/ml"
    mkdir(path)


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


def download_russian_database():
    file_id = '1ftHaSvFz50n7ly5Z-RuyY9_U3qVcWk7G'
    destination = getcwd() + "/ml/russian_database"
    print(destination)
    download_file_from_google_drive(file_id, destination)


def download_vectorized():
    file_id = '104_r57hNblE0hsop2G_T_LBklAl1tBX8'
    destination = getcwd() + "/ml/russian_database.vectors.npy"
    print(destination)
    download_file_from_google_drive(file_id, destination)
