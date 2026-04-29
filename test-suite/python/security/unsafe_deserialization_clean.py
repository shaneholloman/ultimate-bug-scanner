import numpy as np
import pandas as pd
import torch
import yaml


def decode_yaml_payload(payload: str) -> dict:
    return yaml.safe_load(payload)


def load_numeric_array(path: str):
    return np.load(path, allow_pickle=False)


def load_weights_only_checkpoint(path: str):
    return torch.load(path, weights_only=True)


def read_dataframe(path: str):
    return pd.read_parquet(path)
