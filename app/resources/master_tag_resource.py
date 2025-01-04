def tag_resource(tag, columns):
    tag_dict = dict(zip(columns, tag))
    return tag_dict


def tag_value_resource(value, columns):
    tag_dict = dict(zip(columns, value))
    return tag_dict
