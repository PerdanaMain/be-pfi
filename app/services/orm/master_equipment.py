from digital_twin_migration.models.pfi_app import PFIEquipment
from digital_twin_migration.database import Transactional, Propagation
from digital_twin_migration.database import db
from app.resources.master_equipment_resource import equipment_resource
from app.services.response import not_found


def get_all_equipments():
    equipments = PFIEquipment.query.filter_by(parent_id=None).all()
    data = []
    if len(equipments) > 0:
        for eq in equipments:
            data.append(equipment_resource(eq))
    else:
        data = None

    return data


def get_equipment_by_id(id):
    equipment = PFIEquipment.query.filter_by(id=id).first()
    if equipment:
        return equipment_resource(equipment)
    else:
        return None


@Transactional(propagation=Propagation.REQUIRED)
def create_equipment(data):
    try:
        equipment = PFIEquipment(**data)
        equipment.save()
        return None
    except:
        return "Internal Server Error: Unable to create equipment"


@Transactional(propagation=Propagation.REQUIRED)
def update_equipment(id, data):
    try:
        equipment = PFIEquipment.query.filter_by(id=id).first()

        if not equipment:
            return not_found(False, "Master Equipment not found", None)

        for key, value in data.items():
            if hasattr(equipment, key):
                setattr(equipment, key, value)

        db.session.commit()
        return None
    except:
        return "Internal Server Error: Unable to update equipment"


@Transactional(propagation=Propagation.REQUIRED)
def delete_equipment(id):
    try:
        equipment = PFIEquipment.query.filter_by(id=id).first()

        if not equipment:
            return not_found(False, "Master Equipment not found", None)

        db.session.delete(equipment)
        db.session.commit()
        return None
    except:
        return "Internal Server Error: Unable to delete equipment"
