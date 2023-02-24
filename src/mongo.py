import pymongo

from constants import LOGIN_MONGO_PATH
from fs import read_json


def get_login():
    login = read_json(LOGIN_MONGO_PATH)
    return login["username"], login["password"], login["db"]


def get_mongo_client():
    username, pwd, db = get_login()
    return pymongo.MongoClient(f"mongodb+srv://{username}:{pwd}@{db}/?retryWrites=true")


def get_all_malicious_urls():
    return list(map(lambda obj: obj["url"], get_mongo_client()["malicious_url"].urls.find()))


def insert_many_url_to_analyze(list_url):
    return get_mongo_client().url_to_analyze.urls.insert_many(convert_list_url_to_obj_url(list_url))


def convert_list_url_to_obj_url(list_url):
    return [{"url": url} for url in list_url]
