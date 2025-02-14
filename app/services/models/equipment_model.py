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


def get_parent_equipments(parent_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT 
                ms_equipment_master.id,
                ms_equipment_master.parent_id,
                ms_equipment_master.name,
                ms_equipment_master.assetnum,
                ms_equipment_master.location_tag
            FROM ms_equipment_master
            WHERE ms_equipment_master.id = %s
        """

        cursor.execute(sql, (parent_id,))
        equipment_cols = [col[0] for col in cursor.description]
        fetch = cursor.fetchone()
        parent_equipment = dict(zip(equipment_cols, fetch))

        return parent_equipment
    except Exception as e:
        raise Exception(f"Error fetching parent equipments: {e}")


def get_systems():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT *
            FROM ms_equipment_master
            WHERE equipment_tree_id = '75bd4338-5f4d-4441-a5ae-be415505dcc8'
        """

        cursor.execute(sql)
        sub_system_cols = [col[0] for col in cursor.description]
        fetch = cursor.fetchall()

        sub_systems = [dict(zip(sub_system_cols, d)) for d in fetch]
        equipments = get_equipments()

        # Mendapatkan status untuk setiap sistem
        for sub_system in sub_systems:
            status = "normal"  # Status default

            # Cek status equipment di bawah sistem ini
            for equipment in equipments["equipments"]:
                if equipment["parent_id"] == sub_system["id"]:
                    if equipment["status_equipment"] == "predicted failed":
                        status = "predicted failed"
                        break
                    elif (
                        equipment["status_equipment"] == "warning"
                        and status != "predicted failed"
                    ):
                        status = "warning"

            sub_system["sub_sytem_status"] = status

        sql = """
            SELECT *
            FROM ms_equipment_master
            WHERE parent_id IS NULL
        """

        cursor.execute(sql)
        system_cols = [col[0] for col in cursor.description]
        fetch = cursor.fetchall()
        systems = [dict(zip(system_cols, d)) for d in fetch]

        for system in systems:
            status = "normal"
            for sub_system in sub_systems:
                if sub_system["parent_id"] == system["id"]:
                    if sub_system["sub_sytem_status"] == "predicted failed":
                        status = "predicted failed"
                        break
                    elif (
                        sub_system["sub_sytem_status"] == "warning"
                        and status != "predicted failed"
                    ):
                        status = "warning"

            system["system_status"] = status

        return {
            "systems": systems if systems else None,
        }
    except Exception as e:
        raise Exception(f"Error fetching equipments: {e}")


def get_equipments_for_admin(
    tree="53325b34-3f97-4f37-95cc-4a32b9de92de", limit=20, page=1
):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Query untuk mengambil total jumlah parent (untuk total halaman)
        count_sql = (
            "SELECT COUNT(*) FROM ms_equipment_master WHERE equipment_tree_id = %s"
        )
        cursor.execute(count_sql, (tree,))
        total_parents = cursor.fetchone()[0]

        # Hitung total halaman
        total_pages = (total_parents + limit - 1) // limit

        sql = """
            SELECT 
                mem.*
            FROM ms_equipment_master_backup mem
            WHERE equipment_tree_id = %s 
            ORDER BY name ASC
            LIMIT %s OFFSET %s
        """

        cursor.execute(sql, (tree, limit, (page - 1) * limit))

        columns = [col[0] for col in cursor.description]
        equipments = cursor.fetchall()
        equipments = [dict(zip(columns, equipment)) for equipment in equipments]

        return {
            "equipments": equipments if equipments else None,
            "pagination": {
                "page": page,
                "limit": limit,
                "total_pages": total_pages,
                "total_data": total_parents,
            },
        }
    except Exception as e:
        raise Exception(f"Error fetching equipments: {e}")


def search_equipment(name, tree="53325b34-3f97-4f37-95cc-4a32b9de92de"):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        search_pattern = f"%{name}%"

        sql = """
            SELECT * 
            FROM ms_equipment_master_backup
            WHERE name LIKE %s AND equipment_tree_id = %s
            ORDER BY name ASC
        """

        cursor.execute(sql, (search_pattern, tree))
        columns = [col[0] for col in cursor.description]
        equipments = cursor.fetchall()
        equipments = [dict(zip(columns, equipment)) for equipment in equipments]

        return equipments
    except Exception as e:
        raise Exception(f"Error searching equipment: {e}")


def get_equipments():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Query utama dengan subquery untuk status dari pf_details
        sql = """
            WITH EquipmentStatus AS (
                SELECT 
                    p.equipment_id,
                    CASE 
                        WHEN bool_or(pd.predict_status = 'predicted failed') THEN 'predicted failed'
                        WHEN bool_or(pd.predict_status = 'warning') THEN 'warning'
                        ELSE 'normal'
                    END as status_equipment
                FROM pf_parts p
                JOIN pf_details pd ON p.id = pd.part_id
                GROUP BY p.equipment_id
            )
            SELECT DISTINCT ON (em.id) 
                em.*,
                p.id as part_id,
                COALESCE(es.status_equipment, 'normal') as status_equipment
            FROM ms_equipment_master em
            JOIN pf_parts p ON em.id = p.equipment_id
            LEFT JOIN EquipmentStatus es ON em.id = es.equipment_id
            ORDER BY em.id ASC,
                CASE 
                    WHEN es.status_equipment = 'predicted failed' THEN 1
                    WHEN es.status_equipment = 'warning' THEN 2
                    ELSE 3
                END;
        """

        cursor.execute(sql)

        columns = [col[0] for col in cursor.description]
        parents = cursor.fetchall()
        status_priority = {"predicted failed": 0, "warning": 1, "normal": 2}

        result = []
        for parent in parents:
            parent_data = equipment_resource(parent, columns)
            # Ambil status langsung dari hasil query
            status_idx = columns.index("status_equipment")
            parent_data["status_equipment"] = parent[status_idx]

            result.append(parent_data)

        # Urutkan hasil berdasarkan status priority
        sorted_result = sorted(
            result,
            key=lambda x: status_priority.get(x["status_equipment"].lower(), 999),
        )

        return {
            "equipments": sorted_result if sorted_result else None,
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
        parent_data["total_parts"] = len(parts) if parts else None
        result.append(parent_data)

        return {"equipments": result[0]} if result else None

    except Exception as e:
        raise Exception(f"Error fetching equipment: {e}")


def get_report_equipment(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM ms_equipment_master WHERE id = %s"
        cursor.execute(sql, (id,))

        columns = [col[0] for col in cursor.description]
        equipment = cursor.fetchone()

        cursor.close()

        result = dict(zip(columns, equipment))

        return result if result else None

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
