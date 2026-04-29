from flask import request
from joblib import load as load_joblib
from yaml import unsafe_load

import cloudpickle
import dill as serializer
import joblib
import jsonpickle
import marshal
import numpy as np
import pandas as pd
import shelve
import torch
import yaml


def decode_marshal_payload():
    return marshal.loads(request.data)


def decode_dill_payload():
    payload = request.get_data()
    return serializer.loads(payload)


def decode_cloudpickle_file():
    return cloudpickle.load(request.files["payload"])


def load_joblib_artifact():
    return joblib.load(request.files["model"])


def load_joblib_alias():
    return load_joblib(request.args["path"])


def decode_jsonpickle_payload():
    return jsonpickle.decode(request.form["payload"])


def open_shelve_from_request():
    return shelve.open(request.args["db"])


def load_numpy_pickle_array():
    return np.load(request.files["array"], allow_pickle=True)


def load_torch_checkpoint():
    return torch.load(request.files["checkpoint"])


def read_pickled_dataframe():
    return pd.read_pickle(request.files["frame"])


def unsafe_yaml_payload():
    return yaml.unsafe_load(request.data)


def unsafe_yaml_alias():
    return unsafe_load(request.data)
