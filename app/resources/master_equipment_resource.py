def equipment_resource(equipment):
    arr = [
        {
            "id": equipment.id,
            "parent_id": equipment.parent_id,
            "name": equipment.name,
            "description": equipment.path,
        }
    ]

    return arr
