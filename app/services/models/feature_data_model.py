from app.config.database import get_connection


def get_data_values(equipment_id, features_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Query untuk mengambil data
        query = """
            SELECT * FROM dl_features_data_backup WHERE equipment_id = %s AND features_id = %s
        """

        cursor.execute(query, (equipment_id, features_id))

        # Mendapatkan nama kolom
        columns = [col[0] for col in cursor.description]

        # Mendapatkan hasil dari query
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        # Mengonversi setiap tuple menjadi dictionary
        return {
            "values": [dict(zip(columns, d)) for d in data],
        }
    except Exception as e:
        raise Exception(f"Error: {e}")
