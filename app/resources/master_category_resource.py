def category_resource(category):
    return {
        "id": category.id,
        "name": category.name,
        "rigid_or_flexy": category.rigid_or_flexy,
        "edges_a": category.edges_a,
        "edges_b": category.edges_b,
        "edges_c": category.edges_c,
        "edges_d": category.edges_d,
        "created_at": category.created_at,
        "updated_at": category.updated_at,
    }
