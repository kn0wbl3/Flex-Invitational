# from static.test_data import data

def format_tee_data(data, front_or_back):
    showcase = {}
    for tee in data["TeeSets"]:
        entry = {}
        if tee["TeeSetStatus"] != "Active":
            continue
        nine_hole_par = create_nine_hole_par(tee["Holes"], front_or_back)
        key = create_key(tee, nine_hole_par, front_or_back)
        course_rating, slope = get_course_rating_and_slope(tee["Ratings"], front_or_back)
        entry.update({
            "nine_hole_par": nine_hole_par,
            "front_or_back": front_or_back,
            "course_rating": course_rating,
            "slope": slope,
            "tee_color": tee["TeeSetRatingName"]
        })
        showcase.update({key: entry})
    return showcase


def create_key(tee, nine_hole_par, front_or_back):
    sep = " - "
    return tee["Gender"] + sep + tee["TeeSetRatingName"].title() + sep + front_or_back.title() + sep + f"Par: {nine_hole_par}"


def create_nine_hole_par(holes, front_or_back):
    st_hole, end_hole = (0, 9) if front_or_back.lower() == "front" else (9, 18)
    nine_hole_par = sum([x["Par"] for x in holes[st_hole:end_hole]])
    return nine_hole_par


def get_course_rating_and_slope(ratings, front_or_back):
    for rating in ratings:
        if rating["RatingType"].lower() == front_or_back.lower():
            return rating["CourseRating"], rating["SlopeRating"]
    return None
