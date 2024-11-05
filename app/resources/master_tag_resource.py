def tag_resource(tag, columns):
    # Mengonversi tuple ke dictionary menggunakan nama kolom
    tag_dict = dict(zip(columns, tag))
    return tag_dict
