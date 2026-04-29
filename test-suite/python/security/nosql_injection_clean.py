def explicit_field_filter(collection, email):
    normalized_email = str(email).strip().lower()
    return collection.find_one({"email": normalized_email, "active": True})


def allowlisted_sort(collection, status):
    allowed_status = {"open", "closed", "pending"}
    if status not in allowed_status:
        raise ValueError("unsupported status")
    return collection.find({"status": status})


def builtin_dict_fixed_fields(collection, status):
    fixed_filter = dict({"status": status, "archived": False})
    return collection.find_one(fixed_filter)


def safe_update(collection, user_id, display_name):
    return collection.update_one(
        {"_id": user_id},
        {"$set": {"display_name": str(display_name)}},
    )


def static_pipeline(collection, tenant_id):
    pipeline = [
        {"$match": {"tenant_id": tenant_id}},
        {"$project": {"email": 1, "created_at": 1}},
    ]
    return collection.aggregate(pipeline)
