def equipment_resource(equipment):
    return {
        "id": equipment.id,
        "parent_id": equipment.parent_id,
        "name": equipment.name,
        "category": (
            {
                "id": equipment.category.id,
                "name": equipment.category.name,
                "created_at": equipment.category.created_at,
                "updated_at": equipment.category.updated_at,
            }
            if equipment.category
            else None
        ),
        "children": (
            [equipment_resource(child) for child in equipment.children]
            if equipment.children
            else None
        ),
        "created_at": equipment.created_at,
        "updated_at": equipment.updated_at,
    }
