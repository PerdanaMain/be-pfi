from app.config.database import get_connection
from app.resources.feature_resource import feature_resource


def get_oh_schedule_by_year(year):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        SELECT 
            id, start, finish, year
        FROM rp_oh_schedule
        WHERE year >= %s
        ORDER BY year ASC
        LIMIT 1
        """
        cursor.execute(sql, (year,))
        columns = [col[0] for col in cursor.description]
        oh_schedules = cursor.fetchone()

        result = dict(zip(columns, oh_schedules))

        cursor.close()

        return {"oh_schedules": result}
    except Exception as e:
        raise Exception(f"Error fetching features: {e}")
