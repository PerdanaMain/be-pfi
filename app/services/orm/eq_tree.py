from digital_twin_migration.models.pfi_app import PFIEquipmentTree
from digital_twin_migration.database import Transactional, Propagation
from app.resources.eq_tree_resource import eq_tree_resource
from digital_twin_migration.database import db
from app.services.response import not_found


def get_all_trees():
    trees = PFIEquipmentTree.query.all()
    data = []
    if len(trees) > 0:
        for eq in trees:
            data.append(eq_tree_resource(eq))
    else:
        data = None

    return data


def get_tree_by_id(id):
    tree = PFIEquipmentTree.query.filter_by(id=id).first()
    if tree:
        return eq_tree_resource(tree)
    else:
        return None


@Transactional(propagation=Propagation.REQUIRED)
def create_tree(data):
    try:
        tree = PFIEquipmentTree(**data)
        tree.save()
        return None
    except:
        return "Internal Server Error: Unable to create equipment tree"


@Transactional(propagation=Propagation.REQUIRED)
def update_tree(id, data):
    try:
        tree = PFIEquipmentTree.query.filter_by(id=id).first()

        for key, value in data.items():
            if hasattr(tree, key):
                setattr(tree, key, value)

        db.session.commit()
        return None
    except:
        return "Internal Server Error: Unable to update equipment tree"


@Transactional(propagation=Propagation.REQUIRED)
def delete_tree(id):
    try:
        tree = PFIEquipmentTree.query.filter_by(id=id).first()
        if not tree:
            return not_found(False, "Equipment Tree not found", None)
        tree.delete()
        return None
    except:
        return "Internal Server Error: Unable to delete equipment tree"
