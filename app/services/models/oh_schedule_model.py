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
        WHERE year = %s
        """
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        oh_schedules = cursor.fetchall()

        cursor.close()

        return {
            "oh_schedules": (
                [feature_resource(oh_schedule, columns) for oh_schedule in oh_schedules]
                if oh_schedules
                else None
            )
        }
    except Exception as e:
        raise Exception(f"Error fetching features: {e}")
