from app.config.database import get_connection


def get_predict_values(part_id, features_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Query untuk mengambil data
        query = """
            SELECT * FROM dl_predict WHERE part_id = %s AND features_id = %s
            ORDER BY date_time ASC
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


def get_detail(part_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        query = "SELECT * FROM pf_details WHERE part_id = %s"
        cur.execute(query, (part_id,))

        columns = [col[0] for col in cur.description]

        data = cur.fetchone()
        return {
            "details": dict(zip(columns, data)),
        }
    except Exception as e:
        raise Exception(f"An exception occurred: {e}")
