import os
import datetime


def create_dir(path: str) -> None:
    if not (os.path.isdir(path)):
        os.mkdir(path)


def rename_photo(user_id: int, photo_name: str) -> str:
    return f'{str(user_id)}@#%#@{datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M")}@#%#@{photo_name}'


def original_name_photo(photo_name: str) -> str:
    return photo_name.split("@#%#@")[-1]
