from app.config.database import get_connection


def get_data_values(part_id, features_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Query untuk mengambil data
        query = """
            SELECT * FROM dl_features_data WHERE part_id = %s AND features_id = %s
            ORDER BY date_time ASC
        """

        cursor.execute(query, (part_id, features_id))

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


def get_last_data_value(part_id, feature_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Query untuk mengambil data
        query = """
            SELECT * FROM dl_features_data WHERE part_id = %s AND features_id = %s
            ORDER BY date_time DESC LIMIT 1
        """

        cursor.execute(query, (part_id, feature_id))

        # Mendapatkan nama kolom
        columns = [col[0] for col in cursor.description]

        # Mendapatkan hasil dari query
        data = cursor.fetchone()

        cursor.close()
        conn.close()

        # Mengonversi setiap tuple menjadi dictionary
        return data[3]
    except Exception as e:
        raise Exception(f"Error: {e}")
