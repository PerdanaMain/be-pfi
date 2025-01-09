from app.config.database import get_connection
from app.resources.master_equipment_resource import equipment_resource
from app.services.models.eq_tree_model import get_eq_tree_by_id
from app.services.models.part_model import (
    get_parts_by_equipment_id,
    get_parts_by_equpment_id_with_detail,
)
from datetime import datetime
import uuid
import pytz


def get_equipments(page=1, limit=10):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Query untuk mengambil total jumlah parent (untuk total halaman)
        count_sql = """
            SELECT COUNT(DISTINCT ms_equipment_master.id) 
            FROM ms_equipment_master
            JOIN pf_parts ON ms_equipment_master.id = pf_parts.equipment_id;
        """
        cursor.execute(count_sql)
        total_parents = cursor.fetchone()[0]

        # Hitung total halaman
        total_pages = (total_parents + limit - 1) // limit

        # Query untuk mengambil parent dengan paginasi
        sql = """
            SELECT DISTINCT ON (ms_equipment_master.id) 
            ms_equipment_master.*,
            pf_parts.id as part_id
            FROM ms_equipment_master
            JOIN pf_parts ON ms_equipment_master.id = pf_parts.equipment_id
            ORDER BY ms_equipment_master.id ASC;
        """
        cursor.execute(sql, (limit, (page - 1) * limit))

        columns = [col[0] for col in cursor.description]
        parents = cursor.fetchall()

        result = []
        for parent in parents:
            parent_id = parent[columns.index("id")]
            tree_id = parent[columns.index("equipment_tree_id")]

            # Mengambil data anak secara rekursif
            childrens = get_equipment_childrens(parent_id, columns)
            tree = get_eq_tree_by_id(tree_id)
            parts = get_parts_by_equpment_id_with_detail(parent[columns.index("id")])

            # Mengolah data parent
            parent_data = equipment_resource(parent, columns)
            parent_data["childrens"] = childrens if childrens else None
            parent_data["equipment_tree"] = tree if tree else None
            parent_data["parts"] = parts if parts else None

            result.append(parent_data)

        cursor.close()

        return {
            "pagination": {
                "page": page,
                "limit": limit,
                "total_pages": total_pages,
                "total_data": total_parents,
            },
            "equipments": result if result else None,
        }
    except Exception as e:
        raise Exception(f"Error fetching equipments: {e}")


def get_equipments_by_tree_id(equipment_tree_id, page=1, limit=10):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Query untuk mengambil total jumlah parent (untuk total halaman)
        count_sql = (
            "SELECT COUNT(*) FROM ms_equipment_master WHERE equipment_tree_id = %s"
        )
        cursor.execute(count_sql, (equipment_tree_id,))
        total_parents = cursor.fetchone()[0]

        # Hitung total halaman
        total_pages = (total_parents + limit - 1) // limit

        # Query untuk mengambil parent dengan paginasi
        sql = """
            SELECT * 
            FROM ms_equipment_master 
            WHERE equipment_tree_id = %s 
            ORDER BY id ASC 
            LIMIT %s OFFSET %s
        """
        cursor.execute(sql, (equipment_tree_id, limit, (page - 1) * limit))

        columns = [col[0] for col in cursor.description]
        parents = cursor.fetchall()

        result = []
        for parent in parents:
            eq_tree_id = parent[columns.index("equipment_tree_id")]

            # Mengambil data anak secara rekursif
            tree = get_eq_tree_by_id(eq_tree_id)

            # Mengolah data parent
            parent_data = equipment_resource(parent, columns)
            parent_data["equipment_tree"] = tree if tree else None

            result.append(parent_data)

        cursor.close()

        return {
            "pagination": {
                "page": page,
                "limit": limit,
                "total_pages": total_pages,
                "total_data": total_parents,
            },
            "equipments": result if result else None,
        }
    except Exception as e:
        raise Exception(f"Error fetching equipments: {e}")


def get_equipment(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM ms_equipment_master WHERE id = %s"
        cursor.execute(sql, (id,))

        columns = [col[0] for col in cursor.description]
        equipment = cursor.fetchone()

        cursor.close()

        result = []

        tree_id = equipment[columns.index("equipment_tree_id")]
        tree_data = get_eq_tree_by_id(tree_id)
        parts = get_parts_by_equipment_id(id)

        parent_data = equipment_resource(equipment, columns)
        parent_data["equipment_tree"] = tree_data if tree_data else None
        parent_data["parts"] = parts if parts else None
        result.append(parent_data)

        return {"equipments": result[0]} if result else None

    except Exception as e:
        raise Exception(f"Error fetching equipment: {e}")


def get_equipment_childrens(parent_id, columns):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM ms_equipment_master WHERE parent_id = %s"
        cursor.execute(sql, (parent_id,))

        childrens = cursor.fetchall()

        result = []
        for child in childrens:
            child_data = equipment_resource(child, columns) if child else None

            tree_data = get_eq_tree_by_id(child[columns.index("equipment_tree_id")])

            # Jika anak juga memiliki anak, panggil fungsi rekursif
            child_data["childrens"] = (
                get_equipment_childrens(child[columns.index("id")], columns)
                if child[columns.index("parent_id")]
                else None
            )
            child_data["equipment_tree"] = tree_data if tree_data else None

            result.append(child_data)

        cursor.close()

        return result

    except Exception as e:
        raise Exception(f"Error fetching equipment children: {e}")


def create_equipment(
    name,
    equipment_tree_id,
    category_id,
    parent_id=None,
    assetnum=None,
    location_tag=None,
    system_tag=None,
):
    try:
        # Data persiapan
        equipment_id = str(uuid.uuid4())
        timestamp = datetime.now(pytz.timezone("Asia/Jakarta")).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        data = {
            "id": equipment_id,
            "name": name,
            "equipment_tree_id": equipment_tree_id,
            "category_id": category_id,
            "parent_id": parent_id,
            "assetnum": assetnum,
            "location_tag": location_tag,
            "system_tag": system_tag,
            "created_at": timestamp,
            "updated_at": timestamp,
        }

        sql = """
            INSERT INTO ms_equipment_master 
            (id, name, equipment_tree_id, category_id, parent_id, assetnum, location_tag, system_tag, created_at, updated_at) 
            VALUES (%(id)s, %(name)s, %(equipment_tree_id)s, %(category_id)s, %(parent_id)s, %(assetnum)s, %(location_tag)s, %(system_tag)s, %(created_at)s, %(updated_at)s)
        """

        # Eksekusi query
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, data)
                conn.commit()

    except Exception as e:
        raise Exception(f"Error creating equipment: {e}")


def update_equipment(id, data):
    try:
        # Data persiapan
        timestamp = datetime.now(pytz.timezone("Asia/Jakarta")).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        data["updated_at"] = timestamp
        data["id"] = str(id)

        # Filter data yang tidak kosong
        data = {key: value for key, value in data.items() if value is not None}

        # Buat set clause secara dinamis
        set_clause = ", ".join(
            [f"{key} = %({key})s" for key in data.keys() if key != "id"]
        )

        # Query untuk update data
        sql = f"""
            UPDATE ms_equipment_master 
            SET {set_clause} 
            WHERE id = %(id)s
        """

        # Eksekusi query
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, data)
                conn.commit()

    except Exception as e:
        raise Exception(f"Error updating equipment: {e}")


def delete_equipment(id):
    try:
        # Query untuk memastikan record dengan id ada
        check_sql = "SELECT COUNT(*) FROM ms_equipment_master WHERE id = %s"

        # Query untuk menghapus equipment
        delete_sql = "DELETE FROM ms_equipment_master WHERE id = %s"

        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Periksa apakah equipment dengan ID tersebut ada
                cursor.execute(check_sql, (id,))
                count = cursor.fetchone()[0]

                if count == 0:
                    return {
                        "status": False,
                        "message": f"Equipment with ID {id} not found.",
                    }

                # Hapus equipment jika ditemukan
                cursor.execute(delete_sql, (id,))
                conn.commit()

        return {
            "status": True,
            "message": f"Equipment with ID {id} successfully deleted.",
        }

    except Exception as e:
        raise Exception(f"Error deleting equipment: {e}")
