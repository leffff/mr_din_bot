from os import getcwd, mkdir, listdir
import requests


class RussianDataset:
    def __download_file_from_google_drive(self, id, destination):
        URL = "https://docs.google.com/uc?export=download"

        session = requests.Session()

        response = session.get(URL, params={'id': id}, stream=True)
        token = self.__get_confirm_token(response)

        if token:
            params = {'id': id, 'confirm': token}
            response = session.get(URL, params=params, stream=True)

        self.__save_response_content(response, destination)

    def __get_confirm_token(self, response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def __save_response_content(self, response, destination):
        CHUNK_SIZE = 32768
        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    @staticmethod
    def create_directory():
        path = getcwd() + "/ml"
        mkdir(path)

    def __download_russian_database(self):
        file_id = '1ftHaSvFz50n7ly5Z-RuyY9_U3qVcWk7G'
        destination = getcwd() + "/ml/russian_database"
        print(destination)
        self.__download_file_from_google_drive(file_id, destination)

    def __download_vectorized(self):
        file_id = '104_r57hNblE0hsop2G_T_LBklAl1tBX8'
        destination = getcwd() + "/ml/russian_database.vectors.npy"
        print(destination)
        self.__download_file_from_google_drive(file_id, destination)

    def download(self):
        if 'ml' not in listdir(getcwd()):
            self.create_directory()
            self.__download_russian_database()
            self.__download_vectorized()

# d = RussianDataset()
# d.download()