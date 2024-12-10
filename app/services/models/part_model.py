from app.config.database import get_connection
from app.resources.part_resource import part_resource
from app.services.models.feature_model import get_feature


def get_parts():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT * 
            FROM pf_parts
        """
        cursor.execute(sql)

        columns = [col[0] for col in cursor.description]
        parts = cursor.fetchall()

        result = []
        for part in parts:
            part_id = part[columns.index("id")]
            equipment_id = part[columns.index("equipment_id")]

            # Mengambil data anak secara rekursif
            part_data = part_resource(part, columns)

            result.append(part_data)

        cursor.close()

        return result if result else None
    except Exception as e:
        raise e


def get_part(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM pf_parts WHERE id = %s"
        cursor.execute(sql, (id,))

        columns = [col[0] for col in cursor.description]
        part = cursor.fetchone()

        cursor.close()

        if not part:
            return None

        result = []
        data = part_resource(part, columns)
        result.append(data)

        return {"part": result[0]}

    except Exception as e:
        raise Exception(f"Error fetching equipment: {e}")


def get_parts_by_equipment_id(equipment_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT
                pp.*
            FROM pf_parts pp
            WHERE pp.equipment_id = %s;
        """
        cursor.execute(sql, (equipment_id,))

        columns = [col[0] for col in cursor.description]
        parts = cursor.fetchall()

        result = []
        for part in parts:
            part_id = part[columns.index("id")]

            # Mengambil data anak secara rekursif
            part_data = part_resource(part, columns)
            part_data["values"] = get_parts_values(part_id)
            # part_data["feature"] = feature["feature"]

            result.append(part_data)

        cursor.close()

        return result if result else None
    except Exception as e:
        raise e


def get_parts_values(part_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            select distinct on (dfd.features_id) 
                dfd.*
            from dl_features_data dfd 
            where dfd.part_id = %s
            order by dfd.features_id, dfd.date_time;
        """
        cursor.execute(sql, (part_id,))

        columns = [col[0] for col in cursor.description]
        parts = cursor.fetchall()

        result = []
        for part in parts:
            part_id = part[columns.index("id")]
            features_id = part[columns.index("features_id")]
            features = get_feature(features_id)

            # Mengambil data anak secara rekursif
            part_data = part_resource(part, columns)
            part_data["feature"] = features["feature"]
            result.append(part_data)

        cursor.close()

        return result if result else None
    except Exception as e:
        raise e
