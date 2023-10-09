from flask import flash
from datetime import datetime as dt
from dateutil import relativedelta as rd
from . import external
import logging

logger = logging.getLogger(__name__)

def validate_ghin(ghin):
    
    ghin_data = external.get_golfer_data_from_ghin(ghin)
    if not ghin_data or ghin_data['golfers']:
        return False
    return True


def validate_posted_score_1(data):
    """
    takes in the first part of a posted round and confirms if the data is valid
    """
    logger.debug("starting `validate_posted_score_1`")
    for field, val in data.items():
        if val == '':
            flash(f"{field} can't be empty!", category="error")
            logger.debug(f"{field}")
            return False

        if len(val) < 2:
            flash(
                f"{field} can't be smaller than 2 characters", category="error"
            )
            logger.debug(f"{field}")
            return False

        if field == "front_or_back":
            
            if val.upper() not in {"FRONT", "BACK"}:
                flash(f"{field} must be 'Front' or 'Back'!", category="error")
                logger.debug(f"{field}")
                return False

        if field == "date":
            
            date = dt.strptime(val, "%Y-%m-%d").date()
            if date < (dt.now().date() - rd.relativedelta(days=7)):
                flash(
                    f"{field}: Your round has to be played within the last 7 days!",
                    category="error"
                )
                logger.debug(f"{field}")
                return False
            if date > dt.now().date():
                flash(
                    f"{date}: Your round can't be played in the future!",
                    category="error"
                )
                logger.debug(f"{field}")
                return False
    logger.debug("validate_posted_score_1 returned True")
    return True


def validate_posted_score_2(data):
    if not data["gross_score"].isdigit():
        flash(f"Your score needs to be a number!", category="error")
        return False
    if int(data["gross_score"]) < 0:
        flash(f"Your score needs to be positive!", category="error")
        return False