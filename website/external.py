import requests
import os

# THEIR_GHIN = "10963290" #Dan

def get_golfer_data_from_ghin(ghin_number):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json",
    }

    data = {
        "user": {
            "email_or_ghin": os.environ["GHIN_ID"],
            "password": os.environ["GHIN_PWD"],
            "remember_me": "true",
        },
        "token": "nonblank",
    }

    r = requests.post("https://api2.ghin.com/api/v1/golfer_login.json", headers=headers, json=data)

    headers["Authorization"] = "Bearer " + r.json()["golfer_user"]["golfer_user_token"]

    url = "https://api.ghin.com/api/v1/golfers/search.json?per_page=1&page=1&golfer_id=" + ghin_number

    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        data = r.json()
        return data
    return None
    