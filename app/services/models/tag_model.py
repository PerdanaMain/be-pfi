from app.config.database import get_fetch_connection
from app.resources.master_tag_resource import tag_resource


def get_selected_tags(*tag, page=1, limit=10):
    conn = get_fetch_connection()
    cursor = conn.cursor()

    # Hitung total tag yang cocok
    total_query = """
        SELECT COUNT(*) 
        FROM dl_ms_tag
        WHERE id IN (%s)
        """
    in_p = ", ".join(list(map(lambda x: "%s", tag)))
    total_query = total_query % in_p
    cursor.execute(total_query, tag)
    total_count = cursor.fetchone()[0]

    # Query untuk mendapatkan tag dengan paginasi
    query = """
        SELECT * 
        FROM dl_ms_tag
        WHERE id IN (%s)
        LIMIT %s OFFSET %s
        """
    offset = (page - 1) * limit
    query = query % (in_p, "%s", "%s")
    cursor.execute(query, tag + (limit, offset))

    # Mendapatkan nama kolom
    columns = [col[0] for col in cursor.description]

    # Mendapatkan hasil dari query
    tags = cursor.fetchall()

    cursor.close()
    conn.close()

    # Mengonversi setiap tuple menjadi dictionary
    return {
        "pagination": {
            "total": total_count,
            "page": page,
            "limit": limit,
            "total_pages": (total_count // limit)
            + (1 if total_count % limit > 0 else 0),
        },
        "tags": [tag_resource(tag, columns) for tag in tags],
    }
