from digital_twin_migration.models.pfi_app import PFICategory
from digital_twin_migration.database import Transactional, Propagation
from app.resources.master_category_resource import category_resource
from app.services.response import not_found


def get_all_categories():
    categories = PFICategory.query.all()
    data = []
    if len(categories) > 0:
        for ctg in categories:
            data.append(category_resource(ctg))
    else:
        data = None

    return data


@Transactional(propagation=Propagation.REQUIRED)
def create_category(data):
    try:
        category = PFICategory(**data)
        category.save()
        return None
    except:
        return "Internal Server Error: Unable to create category"


@Transactional(propagation=Propagation.REQUIRED)
def delete_category(id):
    try:
        category = PFICategory.query.filter_by(id=id).first()
        if category is None:
            return not_found(False, "Master Category not found", None)

        category.delete()
        return None
    except:
        return "Internal Server Error: Unable to delete category"
