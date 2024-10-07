from app.resources.tag_values_resource import tag_values_resource


def tag_resource(tag, tag_values=False, tag_values_interpolated=False):
    return {
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
        "tag_values": (
            [tag_values_resource(tag_value) for tag_value in tag.tag_values]
            if tag_values
            else None
        ),
    }
