def tag_values_resource(tag_value):
    return {
        "id": tag_value.id,
        "time_stamp": tag_value.time_stamp,
        "value": tag_value.value,
    }
