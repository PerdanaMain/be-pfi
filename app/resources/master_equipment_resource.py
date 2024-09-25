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
        "children": (
            [
                {
                    "id": child.id,
                    "name": child.name,
                    "description": child.description,
                }
                for child in equipment.children
            ]
            if equipment.children
            else None
        ),
        "created_at": equipment.created_at,
        "updated_at": equipment.updated_at,
    }
