from flask import request


def raw_json_filter(collection):
    query = request.get_json()
    return collection.find_one(query)


def copied_request_args(collection):
    filters = request.args.to_dict()
    return collection.find(filters)


def builtin_dict_request_args(collection):
    filters = dict(request.args)
    return collection.delete_many(filters)


def operator_from_json(collection):
    payload = request.json["role"]
    query = {"role": {"$ne": payload}}
    return collection.find_one(query)


def javascript_where(collection):
    where_clause = request.args["where"]
    return collection.find({"$where": where_clause})


def dynamic_field_name(collection):
    field = request.args["field"]
    value = request.args["value"]
    return collection.find_one({field: value})


def aggregation_pipeline(collection):
    match_stage = {"$match": request.get_json()}
    return collection.aggregate([match_stage])


def mongo_command(db):
    return db.command(request.json)
