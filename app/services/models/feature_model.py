from app.config.database import get_connection
from app.resources.feature_resource import feature_resource
from datetime import datetime
import uuid
import pytz


def get_features():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM dl_ms_features"
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        features = cursor.fetchall()

        cursor.close()

        return {
            "features": (
                [feature_resource(feature, columns) for feature in features]
                if features
                else None
            )
        }
    except Exception as e:
        raise Exception(f"Error fetching features: {e}")


def get_feature(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM dl_ms_features WHERE id = %s"
        cursor.execute(sql, (id,))
        columns = [col[0] for col in cursor.description]
        feature = cursor.fetchone()

        cursor.close()

        return {"feature": feature_resource(feature, columns)} if feature else None
    except Exception as e:
        raise Exception(f"Error fetching feature: {e}")


def create_feature(*data):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        feature_id = str(uuid.uuid4())
        name = data[0]
        category = data[1]
        date = datetime.now(pytz.timezone("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M:%S")

        sql = "INSERT INTO dl_ms_features (id, name, category, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (feature_id, name, category, date, date))
        conn.commit()

        cursor.close()

        return {
            "feature": {
                "id": feature_id,
                "name": name,
                "category": category,
            }
        }
    except Exception as e:
        raise Exception(f"Error creating feature: {e}")


def update_feature(id, *data):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        name = data[0]
        category = data[1]
        date = datetime.now(pytz.timezone("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M:%S")

        sql = "UPDATE dl_ms_features SET name = %s, category = %s, updated_at = %s WHERE id = %s"

        cursor.execute(sql, (name, category, date, id))
        conn.commit()

        cursor.close()

        return {
            "feature": {
                "id": id,
                "name": name,
                "category": category,
            }
        }
    except Exception as e:
        raise Exception(f"Error updating feature: {e}")


def delete_feature(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM dl_ms_features WHERE id = %s"
        cursor.execute(sql, (id,))
        conn.commit()

        cursor.close()

        return None
    except Exception as e:
        raise Exception(f"Error deleting feature: {e}")
