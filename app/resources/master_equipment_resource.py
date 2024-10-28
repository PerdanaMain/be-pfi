def equipment_resource(equipment):
    return {
        "id": equipment.id,
        "parent_id": equipment.parent_id,
        "name": equipment.name,
        "system_tag": equipment.system_tag,
        "assetnum": equipment.assetnum,
        "location_tag": equipment.location_tag,
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
        "equipment_tree": (
            {
                "id": equipment.equipment_tree.id,
                "level_no": equipment.equipment_tree.level_no,
                "name": equipment.equipment_tree.name,
                "created_at": equipment.equipment_tree.created_at,
                "updated_at": equipment.equipment_tree.updated_at,
            }
            if equipment.equipment_tree
            else None
        ),
        "parent": (
            {
                "id": equipment.parent.id,
                "name": equipment.parent.name,
                "created_at": equipment.parent.created_at,
                "updated_at": equipment.parent.updated_at,
            }
            if equipment.parent
            else None
        ),
        "created_at": equipment.created_at,
        "updated_at": equipment.updated_at,
    }


def paginate(data, page, per_page):
    total_items = len(data)
    total_pages = (total_items + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = data[start:end]

    return {
        "equipments": paginated_data,
        "pagination": {
            "total_items": total_items,
            "total_pages": total_pages,
            "current_page": page,
            "limit": per_page,
        },
    }
