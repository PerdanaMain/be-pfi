def tag_resource(arr, relation=False):
    arr = [
        {
            "id": tag.id,
            "web_id": tag.web_id,
            "name": tag.name,
            "path": tag.path,
            "descriptor": tag.descriptor,
            "point_class": tag.point_class,
            "point_type": tag.point_type,
            "digital_set_name": tag.digital_set_name,
            "engineering_units": tag.engineering_units,
            "span": tag.span,
            "zero": tag.zero,
            "step": tag.step,
            "future": tag.future,
            "display_digits": tag.display_digits,
            "values": (
                [
                    {
                        "id": value.id,
                        "tag_id": value.tag_id,
                        "time_stamp": value.time_stamp,
                        "value": value.value,
                    }
                    for value in tag.tag_values
                ]
                if relation
                else []
            ),
        }
        for tag in arr
    ]

    return arr
