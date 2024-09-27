from digital_twin_migration.models.pfi_app import PFIMasterTag
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
