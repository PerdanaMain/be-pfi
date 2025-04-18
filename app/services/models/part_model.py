from app.config.database import get_connection
from app.resources.part_resource import part_resource
from app.services.models.feature_model import get_feature
from datetime import datetime


def get_parts():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT * 
            FROM pf_parts
        """
        cursor.execute(sql)

        columns = [col[0] for col in cursor.description]
        parts = cursor.fetchall()

        result = []
        for part in parts:
            part_id = part[columns.index("id")]
            equipment_id = part[columns.index("equipment_id")]

            # Mengambil data anak secara rekursif
            part_data = part_resource(part, columns)

            result.append(part_data)

        cursor.close()

        return result if result else None
    except Exception as e:
        raise e


def get_parts_to_fetch():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT * 
            FROM pf_parts
            WHERE web_id IS NOT NULL
        """
        cursor.execute(sql)

        columns = [col[0] for col in cursor.description]
        parts = cursor.fetchall()

        result = [dict(zip(columns, part)) for part in parts] if parts else None

        cursor.close()

        return result if result else None
    except Exception as e:
        raise e


def get_all_parts():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT 
                mem.name,
                mem.location_tag as equipment_tag,
                pf.id as id,
                pf.part_name,
                pf.location_tag,
                pd.upper_threshold as trip_threshold,
                pd.lower_threshold as alarm_threshold,
                pd.one_hundred_percent_condition as normal_value,
                dmt.id as unit_id,
                dmt.unit,
                pf.created_at,
                pf.updated_at
            FROM pf_parts pf
            LEFT JOIN ms_equipment_master mem ON mem.id = pf.equipment_id
            LEFT JOIN pf_details pd ON pd.part_id = pf.id
            LEFT JOIN dl_ms_type dmt ON dmt.id = pf.type_id
            ORDER by pf.updated_at desc;
        """
        cursor.execute(sql)

        columns = [col[0] for col in cursor.description]
        parts = cursor.fetchall()
        parts = [dict(zip(columns, part)) for part in parts]

        cursor.close()

        return parts if parts else None
    except Exception as e:
        raise e


def get_detail(part_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT * 
            FROM pf_details
            WHERE part_id = %s
        """
        cursor.execute(sql, (part_id,))

        columns = [col[0] for col in cursor.description]
        parts = cursor.fetchone()

        result = dict(zip(columns, parts))

        cursor.close()

        return result if result else None
    except Exception as e:
        raise e


def get_report_parts():
    try:

        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            WITH rp_oh_schedule AS (
                SELECT *
                FROM rp_oh_schedule
                WHERE year = '2025'
            )
            SELECT 
                ms_equipment_master.id as equipment_id,
                ms_equipment_master.name as equipmentName,
                ms_equipment_master.location_tag as equipmentTag,
                ms_equipment_master.parent_id as parent_id,
                pf_parts.id,
                pf_parts.equipment_id, 
                pf_parts.part_name as sensorName,
                pf_parts.type_id,
                pf_parts.web_id,
                pf_parts.location_tag as sensorTag,
                pf_details.upper_threshold as tripThreshold,
                pf_details.lower_threshold as alarmThreshold,
                pf_details.time_failure as PFInterval,
                pf_details.predict_status as status,
                dl_ms_type.unit as unit,
                dl_features_data.value as currentValue,
                dl_features_data.date_time as currentValueDate,
                rp_oh_schedule.start as wostart,
                rp_oh_schedule.finish as wofinish,
                rp_oh_schedule.year as woyear
            FROM pf_parts
            JOIN pf_details ON pf_details.part_id = pf_parts.id
            JOIN ms_equipment_master ON ms_equipment_master.id = pf_parts.equipment_id
            JOIN dl_ms_type ON dl_ms_type.id = pf_parts.type_id
            JOIN (
                SELECT DISTINCT ON (part_id) 
                    part_id, value, date_time
                FROM dl_features_data
                ORDER BY part_id, date_time DESC
            ) dl_features_data ON dl_features_data.part_id = pf_parts.id
            CROSS JOIN rp_oh_schedule
            GROUP BY 
                ms_equipment_master.id,
                ms_equipment_master.name,
                ms_equipment_master.location_tag,
                pf_parts.id,
                pf_parts.equipment_id,
                pf_parts.part_name,
                pf_parts.type_id,
                pf_parts.location_tag,
                pf_details.upper_threshold,
                pf_details.lower_threshold,
                pf_details.time_failure,
                pf_details.predict_status,
                dl_ms_type.unit,
                dl_features_data.value,
                dl_features_data.date_time,
                rp_oh_schedule.start,
                rp_oh_schedule.finish,
                rp_oh_schedule.year
            ORDER BY  ms_equipment_master.name asc;
        """
        cursor.execute(sql)

        columns = [col[0] for col in cursor.description]
        parts = cursor.fetchall()

        result = [dict(zip(columns, row)) for row in parts] if parts else None

        cursor.close()

        return result if result else None
    except Exception as e:
        raise e


def get_filtered_report_parts(eq_id, sensor_type, oh_schedules):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Add filter conditions
        params = []

        # Base SQL query
        sql = """
            WITH rp_oh_schedule AS (
                SELECT *
                FROM rp_oh_schedule
                WHERE year = %s
            )
        """
        params.append(oh_schedules["oh_schedules"]["year"])

        sql += """
            SELECT 
                ms_equipment_master.id as equipment_id,
                ms_equipment_master.name as equipmentName,
                ms_equipment_master.location_tag as equipmentTag,
                ms_equipment_master.parent_id as parent_id,
                pf_parts.id,
                pf_parts.equipment_id, 
                pf_parts.part_name as sensorName,
                pf_parts.type_id,
                pf_parts.web_id,
                pf_parts.location_tag as sensorTag,
                pf_details.upper_threshold as tripThreshold,
                pf_details.lower_threshold as alarmThreshold,
                pf_details.time_failure as PFInterval,
                pf_details.predict_status as status,
                dl_ms_type.unit as unit,
                dl_features_data.value as currentValue,
                dl_features_data.date_time as currentValueDate,
                rp_oh_schedule.start as wostart,
                rp_oh_schedule.finish as wofinish,
                rp_oh_schedule.year as woyear
            FROM pf_parts
            JOIN pf_details ON pf_details.part_id = pf_parts.id
            JOIN ms_equipment_master ON ms_equipment_master.id = pf_parts.equipment_id
            JOIN dl_ms_type ON dl_ms_type.id = pf_parts.type_id
            JOIN (
                SELECT DISTINCT ON (part_id) 
                    part_id, value, date_time
                FROM dl_features_data
                ORDER BY part_id, date_time DESC
            ) dl_features_data ON dl_features_data.part_id = pf_parts.id
            CROSS JOIN rp_oh_schedule
            WHERE 1=1
        """

        if eq_id:
            sql += " AND ms_equipment_master.id = %s"
            params.append(eq_id)

        if sensor_type:
            if sensor_type == "DCS":
                sql += " AND pf_parts.web_id IS NOT NULL"
            else:
                sql += " AND pf_parts.web_id IS NULL"

        # Complete the SQL query
        sql += """
            GROUP BY 
                ms_equipment_master.id,
                ms_equipment_master.name,
                ms_equipment_master.location_tag,
                ms_equipment_master.parent_id,
                pf_parts.id,
                pf_parts.equipment_id,
                pf_parts.part_name,
                pf_parts.type_id,
                pf_parts.web_id,
                pf_parts.location_tag,
                pf_details.upper_threshold,
                pf_details.lower_threshold,
                pf_details.time_failure,
                pf_details.predict_status,
                dl_ms_type.unit,
                dl_features_data.value,
                dl_features_data.date_time,
                rp_oh_schedule.start,
                rp_oh_schedule.finish,
                rp_oh_schedule.year
            ORDER BY ms_equipment_master.name asc;
        """

        print(sql)

        # Execute the query with parameters
        cursor.execute(sql, params)

        columns = [col[0] for col in cursor.description]
        parts = cursor.fetchall()

        result = [dict(zip(columns, row)) for row in parts] if parts else None

        cursor.close()

        return result if result else None
    except Exception as e:
        raise e


def get_parts_by_equpment_id_with_detail(equipment_id):
    try:

        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT pf_parts.*, pf_details.* 
            FROM pf_parts
            JOIN pf_details ON pf_details.part_id = pf_parts.id
            WHERE equipment_id = %s
        """
        cursor.execute(sql, (equipment_id,))

        columns = [col[0] for col in cursor.description]
        parts = cursor.fetchall()

        result = []
        for part in parts:
            part_id = part[columns.index("id")]
            equipment_id = part[columns.index("equipment_id")]

            values = get_parts_values(part_id)

            # Mengambil data anak secara rekursif
            part_data = part_resource(part, columns)
            part_data["values"] = values

            result.append(part_data)

        cursor.close()

        return result if result else None
    except Exception as e:
        raise e


def get_part(id):
    try:
        from app.services.models.equipment_model import get_equipment

        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        SELECT 
            mem.name,
            pf.*,
            pd.upper_threshold as trip_threshold,
            pd.lower_threshold as alarm_threshold,
            pd.one_hundred_percent_condition as normal_value,
            dl_ms_type.unit
        FROM pf_parts pf
        JOIN dl_ms_type ON pf.type_id = dl_ms_type.id
        JOIN ms_equipment_master mem ON mem.id = pf.equipment_id
        JOIN pf_details pd ON pd.part_id = pf.id
        WHERE pf.id = %s 
        """

        cursor.execute(sql, (id,))

        columns = [col[0] for col in cursor.description]
        part = cursor.fetchone()

        if not part:
            return None

        # Konversi part ke dictionary
        part_data = part_resource(part, columns)

        # Ambil equipment data dan tambahkan ke part
        equipment_id = part[columns.index("equipment_id")]
        equipment = get_equipment(equipment_id)

        # Tambahkan equipment ke part_data
        part_data["equipment"] = equipment["equipments"]["name"]

        return {"part": part_data}

    except Exception as e:
        raise Exception(f"Error fetching equipment: {e}")


def get_parts_by_equipment_id(equipment_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT pp.*, pd.upper_threshold, pd.lower_threshold, pd.predict_status, dmt.unit
            FROM pf_parts pp
            LEFT JOIN dl_ms_type dmt ON dmt.id = pp.type_id
            LEFT JOIN (
                SELECT DISTINCT ON (part_id) 
                    part_id,
                    upper_threshold,
                    lower_threshold,
                    predict_status
                FROM pf_details
                ORDER BY part_id, id DESC
            ) pd ON pd.part_id = pp.id
            WHERE pp.equipment_id = %s
            order by pp.part_name asc;
        """
        cursor.execute(sql, (equipment_id,))

        columns = [col[0] for col in cursor.description]
        parts = cursor.fetchall()

        result = []
        for part in parts:
            part_id = part[columns.index("id")]

            # Mengambil values
            values = get_parts_values(part_id)

            if values:
                # Membuat salinan part untuk setiap value
                for value in values:
                    part_data = part_resource(
                        part, columns
                    )  # Membuat salinan baru dari part
                    part_data["values"] = [value]  # Menetapkan single value
                    result.append(part_data)
            else:
                # Jika tidak ada values, tetap masukkan part dengan values kosong
                part_data = part_resource(part, columns)
                part_data["values"] = []
                result.append(part_data)

        cursor.close()
        return result if result else None
    except Exception as e:
        raise e


def get_parts_values(part_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            select distinct on (dfd.features_id) 
                dfd.*
            from dl_features_data dfd 
            where dfd.part_id = %s
            order by dfd.features_id, dfd.date_time;
        """
        cursor.execute(sql, (part_id,))

        columns = [col[0] for col in cursor.description]
        parts = cursor.fetchall()

        result = []
        for part in parts:
            features_id = part[columns.index("features_id")]
            features = get_feature(features_id)

            part_data = part_resource(part, columns)
            part_data["feature"] = features["feature"]
            result.append(part_data)

        cursor.close()
        return result if result else None
    except Exception as e:
        raise e


def update_part(id, data):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        now = datetime.now()

        sql = """
            UPDATE pf_parts
            SET 
                part_name = %s,
                location_tag = %s,
                type_id = %s,
                updated_at = %s
            WHERE id = %s
        """
        cursor.execute(
            sql,
            (
                data["part_name"],
                data["location_tag"],
                data["unit_id"],
                now,
                id,
            ),
        )
        conn.commit()

        sql = """
        UPDATE pf_details
        SET 
            upper_threshold = %s,
            lower_threshold = %s,
            one_hundred_percent_condition = %s,
            updated_at = %s
        WHERE part_id = %s
        """

        cursor.execute(
            sql,
            (
                data["trip_threshold"],
                data["alarm_threshold"],
                data["normal_value"],
                now,
                id,
            ),
        )
        conn.commit()

        cursor.close()
        return True
    except Exception as e:
        raise e
