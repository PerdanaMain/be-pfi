from app.config.database import get_connection


def get_eq_tree_by_id(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT id, level_no, name FROM ms_equipment_tree WHERE id = %s"
        cursor.execute(sql, (str(id),))

        columns = [col[0] for col in cursor.description]
        equipment_tree = cursor.fetchone()

        cursor.close()

        return {
            "id": equipment_tree[columns.index("id")],
            "level_no": equipment_tree[columns.index("level_no")],
            "name": equipment_tree[columns.index("name")],
        }
    except Exception as e:
        raise Exception(f"Error fetching equipment tree: {e}")


def get_eq_tree_by_level(level_no):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT id,level_no FROM ms_equipment_tree WHERE level_no = %s"
        cursor.execute(sql, (level_no,))

        columns = [col[0] for col in cursor.description]
        equipment_tree = cursor.fetchone()

        cursor.close()

        return {
            "id": equipment_tree[columns.index("id")],
            "level_no": equipment_tree[columns.index("level_no")],
        }
    except Exception as e:
        raise Exception(f"Error fetching equipment tree: {e}")
