def equipment_resource(equipment):
    return {
        "id": equipment.id,
        "parent_id": equipment.parent_id,
        "name": equipment.name,
        "description": equipment.description,
        "category": (
            {
                "id": equipment.category.id,
                "name": equipment.category.name,
            }
            if equipment.category
            else None
        ),
        "created_at": equipment.created_at,
        "updated_at": equipment.updated_at,
    }
