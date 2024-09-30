from digital_twin_migration.models.pfi_app import PFIMasterTag, PFIValueTag
from app.resources.master_tag_resource import tag_resource
from digital_twin_migration.database import Transactional, Propagation


def get_tag_values_by_date(start_date, end_date):
    tags = PFIMasterTag.query.all()
    data = []
    if len(tags) > 0:
        for tag in tags:
            data.append(tag_resource(tag))
    else:
        data = None

    return data


@Transactional(propagation=Propagation.REQUIRED)
def create_many(data):
    try:
        for item in data:
            tag = PFIValueTag(**item)
            tag.save()
        return None
    except:
        return "Internal Server Error: Unable to create tags"
