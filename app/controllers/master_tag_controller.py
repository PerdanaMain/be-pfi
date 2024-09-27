from app.services.response import success, bad_request
from app.services.orm.master_tag import get_all_tags
from app.services.files.read import read_excel
from app.services.orm.master_tag import mass_insert, exists_tag


def index():
    try:
        data = get_all_tags()
        return success(True, "Master Tags retrieved successfully", data)
    except Exception as e:
        return bad_request(False, str(e), None)


def insert():
    try:
        data = read_excel("API_PI_Tag.xlsx")

        filter_data = [tag for tag in data if exists_tag(tag["web_id"]) is None]
        return success(True, "Master Tags inserted successfully", filter_data)
    except Exception as e:
        return bad_request(False, str(e), None)
