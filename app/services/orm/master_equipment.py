from digital_twin_migration.models.pfi_app import PFIEquipment
from digital_twin_migration.database import Transactional, Propagation
from app.resources.master_equipment_resource import equipment_resource


def get_all_equipments():
    equipments = PFIEquipment.query.all()
    data = []
    if len(equipments) > 0:
        for eq in equipments:
            data.append(equipment_resource(eq))
    else:
        data = None

    return data


@Transactional(propagation=Propagation.REQUIRED)
def create_equipment(data):
    try:
        equipment = PFIEquipment(**data)
        equipment.save()
        return None
    except:
        return "Internal Server Error: Unable to create equipment"
