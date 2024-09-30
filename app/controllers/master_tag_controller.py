from app.services.response import success, bad_request
from app.services.orm.master_tag import get_all_tags
from app.services.files.read import read_excel
from app.services.orm.master_tag import get_all_tags, create_many


def index():
    try:
        data = get_all_tags()
        return success(True, "Master Tags retrieved successfully", data)
    except Exception as e:
        return bad_request(False, str(e), None)


def mass_insert():
    try:
        tags = read_excel("API_PI_Tag.xlsx")
        for tag in tags:
            create_many(tag)
        return success(True, "Master Tags inserted successfully", None)
    except Exception as e:
        return bad_request(False, str(e), None)
