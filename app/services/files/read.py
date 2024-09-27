import os
import json
import pandas as pd


def read_json(fpath):
    path = os.path.join(os.path.dirname(__file__), f"../../../public/{fpath}")
    path = os.path.abspath(path)

    with open(path, "r") as file:
        data = json.load(file)

    return data


def read_excel(fpath):
    path = os.path.join(os.path.dirname(__file__), f"../../../public/{fpath}")
    path = os.path.abspath(path)

    df = pd.read_excel(path)
    data = df.to_dict(orient="records")
    return data
