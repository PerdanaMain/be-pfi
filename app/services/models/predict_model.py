from app.config.database import get_connection


def get_predict_values(part_id, features_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Query untuk mengambil data
        query = """
            SELECT * FROM dl_predict WHERE part_id = %s AND features_id = %s
        """

        cursor.execute(query, (part_id, features_id))

        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return {
            "predictions": [dict(zip(columns, d)) for d in data],
        }
    except Exception as e:
        raise Exception(f"Error: {e}")
