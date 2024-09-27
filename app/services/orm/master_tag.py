from digital_twin_migration.models.pfi_app import PFIMasterTag, PFIValueTag
from app.resources.master_tag_resource import tag_resource
from digital_twin_migration.database import Transactional, Propagation
from digital_twin_migration.database import db


def get_all_tags():
    tags = PFIMasterTag.query.all()
    data = []
    if len(tags) > 0:
        for tag in tags:
            data.append(tag_resource(tag))
    else:
        data = None

    return data


def exists_tag(web_id):
    tag = PFIMasterTag.query.filter_by(web_id=web_id).first()
    return tag


def get_tag_values_by_date(tags, start_date, end_date):
    query = (
        db.session.query(PFIMasterTag)
        .join(PFIValueTag)
        .filter(PFIMasterTag.id.in_(tags))
    )

    if start_date and end_date:
        if start_date == end_date:
            end_date = end_date.replace(
                hour=23, minute=59, second=59, microsecond=999999
            )

        query = query.filter(
            PFIValueTag.time_stamp >= start_date,
            PFIValueTag.time_stamp <= end_date,
        )

    tag_values = query.all()

    if tag_values:
        data = [tag_resource(tag) for tag in tag_values]
    else:
        data = None

    return data


@Transactional(propagation=Propagation.REQUIRED)
def mass_insert(data):
    try:
        # for tag in data:
        #     tag = PFIMasterTag(**tag)
        #     tag.save()

        return True
    except:
        return False
