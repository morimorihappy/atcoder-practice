from __future__ import annotations

import json

import numpy as np


def approx_diff(diffs: list[int | None]) -> list[int]:
    # -1800 ~ 400 is compressed
    original = np.linspace(-1800, 399, 2200)
    modified = np.exp(np.linspace(0, np.log(400), 2200))
    v = np.array(diffs)
    mask = v < 400
    v[mask] = modified[np.searchsorted(original, v[mask], side="left")].copy()
    v[np.isnan(v)] = -1
    return v.astype(np.int32).tolist()


def fetch_diff():
    with open("misc/difficulties.json", mode="r") as f:
        data = json.load(f)

    for k, v in data.items():
        data[k] = approx_diff([vv if vv is not None else np.nan for vv in v])

    return data


def create_table(data: dict[str, list[int]]):
    for i in reversed(range(200, 301)):
        s = f"|ABC{i}|"
        for c, diff in zip(["a", "b", "c", "d"], data[f"abc{i}"]):
            s += f"Diff {diff if diff > -1 else '??'} / xx (xx min)|"

        print(s)


if __name__ == "__main__":
    data = fetch_diff()
    create_table(data)
