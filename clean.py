"""
Read ideals and betti tables from Macaulay2 output and encode into matrices
"""

import ast
from typing import Iterable, List
import json
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


def monomial_to_expvec(m: str, variables: Iterable[str] = ("x", "y", "z")) -> List[int]:
    """
    Takes in formatted monomials and outputs vector of exponents

    :param m: monomial
    :type m: str
    :param variables: formal variables in ideal
    :type variables: Iterable[str]
    :return: vector of exponents corresponding to monomial
    :rtype: List[int]
    """
    var_list = list(variables)
    idx = {v: i for i, v in enumerate(var_list)}
    exps = [0] * len(var_list)

    s = m.replace(" ", "")
    if s == "" or s == "1":
        return exps

    for f in s.split("*"):
        if f == "" or f == "1":
            continue
        if "^" in f:
            base, e = f.split("^", 1)
            if base not in idx:
                raise ValueError(f"unknown variable {base!r}")
            exps[idx[base]] += int(e)
        else:
            if f not in idx:
                raise ValueError(f"unknown variable {f!r}")
            exps[idx[f]] += 1

    return exps


def str_to_matrix(ideal_str: list[str]):
    """
    takes in generators as list of monomials and converts to matrix

    :param ideal_str: Description
    :type ideal_str: str
    """
    return list(
        monomial_to_expvec(generator, variables=("x", "y")) for generator in ideal_str
    )


def brace_string_to_list(s: str):
    """
    Converts betti table from string literal to matrix
    ex: "{{1, 0}, {0, 0}, ...}" -> [[1, 0], [0, 0], ...]

    :param s: betti table in string format
    :type s: str
    """
    t = s.strip().replace("{", "[").replace("}", "]")
    return ast.literal_eval(t)


def pad_with_mask(B: list[int], H: int):
    B = np.asarray(B, dtype=float)
    h = B.shape[0]
    out = np.zeros((H, 2), dtype=float)
    mask = np.zeros((H, 2), dtype=float)
    out[:h, :] = B
    mask[:h, :] = 1.0
    return np.concatenate([out.ravel(), mask.ravel()])  # length 4H


if __name__ == "__main__":
    FILEPATH = "generated/ideals.json"
    try:
        with open(FILEPATH, "r", encoding="utf8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{FILEPATH}' was not found.")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON from {FILEPATH}: {e}")

    ideal_vectors = list()
    betti_matrices = list()
    for key in data:
        ideal = key[9:-2].split(",")
        # print(key[9:-2])
        ideal_mtx = str_to_matrix(ideal)
        ideal_vectors.append(ideal_mtx)
        # print(ideal_mtx)

        betti = data[key][7:]
        betti_mtx = brace_string_to_list(betti)
        betti_matrices.append(betti_mtx)
        # print(betti_mtx)

    # make betti tables uniform size
    max_height = max(len(x) for x in betti_matrices)
    Y = np.stack([pad_with_mask(B, max_height) for B in betti_matrices])

    # append true height of table to ideal data
    X_base = np.asarray(ideal_vectors, dtype=float).reshape(len(ideal_vectors), -1)

    # Y: list of (height_i, 2) betti tables
    heights = np.array(
        [np.asarray(B).shape[0] for B in betti_matrices], dtype=float
    ).reshape(-1, 1)

    # add betti table dimension data to ideal vectors
    X = np.concatenate([X_base, heights], axis=1)  # (n, 5)

    # split into training/testing sets
    Xtr, Xte, Ytr, Yte = train_test_split(X, Y, test_size=0.2, random_state=0)

    regressor = RandomForestRegressor(n_estimators=500, random_state=0, oob_score=True)
    regressor.fit(X, Y)

    Yhat = regressor.predict(Xte)

    print("test MSE:", mean_squared_error(Yte, Yhat))
    print("test R2 :", r2_score(Yte, Yhat))
