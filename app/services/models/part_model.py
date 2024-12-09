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


def get_parts_by_equipment_id(equipment_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT DISTINCT ON (dfd.features_id) 
                pp.*, dfd.part_id, dfd.features_id, dfd.value, dfd.date_time
            FROM pf_parts pp
            JOIN dl_features_data dfd ON pp.id = dfd.part_id
            WHERE pp.equipment_id = %s
            ORDER BY dfd.features_id, dfd.date_time DESC;
        """
        cursor.execute(sql, (equipment_id,))

        columns = [col[0] for col in cursor.description]
        parts = cursor.fetchall()

        result = []
        for part in parts:
            part_id = part[columns.index("id")]
            feature = get_feature(part[columns.index("features_id")])

            # Mengambil data anak secara rekursif
            part_data = part_resource(part, columns)
            part_data["feature"] = feature["feature"]

            result.append(part_data)

        cursor.close()

        return result if result else None
    except Exception as e:
        raise e
