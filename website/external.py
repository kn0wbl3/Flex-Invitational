import requests
import os
import pprint
import logging
import sys

HEADERS = {
    "Content-Type": "application/json; charset=utf-8",
    "Accept": "application/json",
}
BASE_URL = "https://api.ghin.com/api/v1"


pp = pprint.PrettyPrinter(indent=4)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

def login_user():
    logger.debug("starting `login_user`")
    data = {
        "user": {
            "email_or_ghin": os.environ["GHIN_ID"],
            "password": os.environ["GHIN_PWD"],
            "remember_me": "true",
        },
        "token": "nonblank",
    }

    r = requests.post("https://api2.ghin.com/api/v1/golfer_login.json", headers=HEADERS, json=data)

    HEADERS["Authorization"] = "Bearer " + r.json()["golfer_user"]["golfer_user_token"]


def get_golfer_data_from_ghin(ghin_number):
    logger.debug(f"starting `get_golfer_data_from_ghin` with {ghin_number}")
    if not is_logged_in():
        login_user()
    
    url = f"{BASE_URL}/golfers/search.json?per_page=1&page=1&golfer_id={ghin_number}"
    r = requests.get(url, headers=HEADERS)

    if r.status_code == 200:
        return r.json()
    return None


def get_course_data(course_name, course_state):
    logger.debug(f"starting `get_course_data` with {course_name} in {course_state}")
    # To be deleted
    course_state = "US-" + course_state
    
    if not is_logged_in():
        login_user()

    url = f"{BASE_URL}/courses/search.json?name={course_name}&state={course_state}"

    r = requests.get(url, headers=HEADERS)

    if r.status_code == 200:
        data = r.json()
        if data["courses"]:
            return data["courses"][0]["CourseID"]
    return None
    

def get_tee_ratings(course_id):
    logger.debug(f"starting `get_tee_ratings` with {course_id}")
    if not is_logged_in():
        login_user()
    
    url = f"{BASE_URL}/courses/{course_id}/tee_set_ratings.json"

    r = requests.get(url, headers=HEADERS)

    if r.status_code == 200:
        return r.json()
    return None


def is_logged_in():
    logger.debug("starting `is_logged_in`")
    return HEADERS.get("Authorization")
