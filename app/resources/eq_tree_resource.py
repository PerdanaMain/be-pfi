def eq_tree_resource(trees):
    return {
        "id": trees.id,
        "level_no": trees.level_no,
        "name": trees.name,
        "created_at": trees.created_at,
        "updated_at": trees.updated_at,
    }
