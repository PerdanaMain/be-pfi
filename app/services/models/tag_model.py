from app.config.database import get_fetch_connection
from app.resources.master_tag_resource import tag_resource, tag_value_resource


def get_all_tags(page=1, limit=10):
    conn = get_fetch_connection()
    cursor = conn.cursor()

    # Hitung total tag
    total_query = "SELECT COUNT(*) FROM dl_ms_tag"
    cursor.execute(total_query)
    total_count = cursor.fetchone()[0]

    # Query untuk mendapatkan tag dengan paginasi
    query = "SELECT * FROM dl_ms_tag LIMIT %s OFFSET %s"
    offset = (page - 1) * limit
    cursor.execute(query, (limit, offset))

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


def get_tag_by_id(tag_id):
    conn = get_fetch_connection()
    cursor = conn.cursor()

    # Hitung total tag
    query = """
        SELECT * FROM dl_ms_tag WHERE id = %s
        """

    cursor.execute(query, (tag_id,))
    # Mendapatkan nama kolom
    columns = [col[0] for col in cursor.description]

    # Mendapatkan hasil dari query
    tag = cursor.fetchone()
    print(tag)

    cursor.close()
    conn.close()

    # Mengonversi setiap tuple menjadi dictionary
    return {
        "tag": tag_resource(tag, columns) if tag else None,
    }


from datetime import datetime


def get_tag_values(tag_id):
    """
    Ambil data berdasarkan `tag_id` dari database.
    """
    try:
        conn = get_fetch_connection()
        cursor = conn.cursor()

        query = """
            SELECT 
                dl_value_tag.time_stamp AS timestamp,
                dl_value_tag.value AS value
            FROM dl_value_tag
            WHERE dl_value_tag.tag_id = %s
        """
        cursor.execute(query, (tag_id,))
        columns = [col[0] for col in cursor.description]
        results = cursor.fetchall()

        # Ubah hasil menjadi list of dictionaries
        tag_values = []
        for row in results:
            record = dict(zip(columns, row))
            # Konversi timestamp ke string
            if isinstance(record["timestamp"], datetime):
                record["timestamp"] = record["timestamp"].isoformat()  # Format ISO 8601
            tag_values.append(record)

        return tag_values
    except Exception as e:
        print(f"Database Error: {e}")  # Log error
        return None
    finally:
        # Pastikan koneksi ditutup
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_predicted_values(tag_id):
    """
    Ambil data berdasarkan `tag_id` dari database.
    """
    try:
        conn = get_fetch_connection()
        cursor = conn.cursor()

        query = """
            SELECT 
                dl_predict_tag.time_stamp AS timestamp,
                dl_predict_tag.value AS value
            FROM dl_predict_tag
            WHERE dl_predict_tag.tag_id = %s
        """
        cursor.execute(query, (tag_id,))
        columns = [col[0] for col in cursor.description]
        results = cursor.fetchall()

        # Ubah hasil menjadi list of dictionaries
        predict_values = []
        for row in results:
            record = dict(zip(columns, row))
            # Konversi timestamp ke string
            if isinstance(record["timestamp"], datetime):
                record["timestamp"] = record["timestamp"].isoformat()  # Format ISO 8601
            predict_values.append(record)

        return predict_values
    except Exception as e:
        print(f"Database Error: {e}")  # Log error
        return None
    finally:
        # Pastikan koneksi ditutup
        if cursor:
            cursor.close()
        if conn:
            conn.close()


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


def get_psd_values(tag_id):
    conn = get_fetch_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            dl_psd_value.tag_id AS tag_id,
            dl_psd_value.created_at AS timestamp,
            dl_psd_value.psd_value AS value,
            dl_ms_tag.name AS tag_name,
            dl_ms_tag.descriptor AS tag_description
        FROM dl_psd_value
        JOIN dl_ms_tag ON dl_psd_value.tag_id = dl_ms_tag.id
        WHERE dl_psd_value.tag_id = %s
        """
    cursor.execute(query, (tag_id,))
    columns = [col[0] for col in cursor.description]
    psd_values = cursor.fetchall()

    cursor.close()
    conn.close()

    # Membuat array psd_values hanya dengan timestamp dan value
    filtered_psd_values = [
        {
            "timestamp": psd_value[columns.index("timestamp")],
            "value": psd_value[columns.index("value")],
        }
        for psd_value in psd_values
    ]

    return {
        "psd_values": filtered_psd_values,
        "tag": {
            "id": psd_values[0][columns.index("tag_id")] if psd_values else None,
            "name": psd_values[0][columns.index("tag_name")] if psd_values else None,
            "description": (
                psd_values[0][columns.index("tag_description")] if psd_values else None
            ),
        },
    }
