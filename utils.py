def serialize_merch(merch):
    return {
        'id': merch.id,
        'name': merch.name,
        'category': merch.category,
        'price': merch.price,
        'description': merch.description,
        'images': [img.url for img in merch.images]
    }