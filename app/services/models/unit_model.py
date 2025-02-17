from app.config.database import get_connection


def get_units():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT * 
            FROM dl_ms_type
        """
        cursor.execute(sql)

        columns = [col[0] for col in cursor.description]
        units = cursor.fetchall()
        units = [dict(zip(columns, unit)) for unit in units]

        cursor.close()

        return units if units else None
    except Exception as e:
        raise e
