from flask import flash
from datetime import datetime as dt
from dateutil import relativedelta as rd
from . import external

def validate_ghin(ghin):
    ghin_data = external.get_golfer_data_from_ghin(ghin)
    if not ghin_data:
        return False
    if not ghin_data['golfers']:
        return False
    return True


def validate_posted_score(data):
    """
    takes in the round posted by the user and validates the data
    """
    for field, val in data.items():
        if val == '':
            flash(f"{field} can't be empty!", category="error")
            return False

        if len(val) < 2:
            flash(
                f"{field} can't be smaller than 2 characters", category="error"
            )
            return False

        if field == "Front/Back":
            if val.upper() not in {"FRONT", "BACK"}:
                flash(f"{field} must be 'Front' or 'Back'!", category="error")
                return False

        if field == "Slope":
            if int(val) < 55 or int(val) > 155:
                flash(
                    f"{field} seems to be incorrect, double check for 9-hole {field}",
                    category="error"
                )
                return False
        
        if field == "Course Rating":
            if int(val) > 45:
                flash(
                    f"{field} seems to be incorrect, double check for 9-hole {field}",
                    category="error"
                )
                return False

        if field == "Date":
            date = dt.strptime(val, "%Y-%m-%d").date()
            if date < (dt.now().date() - rd.relativedelta(days=7)):
                flash(
                    f"{field}: Your round has to be played within the last 7 days!",
                    category="error"
                )
                return False
            if date > dt.now().date():
                flash(
                    f"{date}: Your round can't be played in the future!",
                    category="error"
                )
                return False
        
        if field == "Score":
            if not val.isdigit():
                flash(
                    f"Your {field} needs to be a number!",
                    category="error"
                )
                return False
        
        if field == "Attestor":
            # need to check the attestors against the active User database
            pass
    return True
        
        