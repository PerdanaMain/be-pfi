def equipment_resource(equipment, columns):
    return dict(zip(columns, equipment))


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
