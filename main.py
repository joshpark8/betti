"""
Read ideals and betti tables from Macaulay2 output and encode into matrices
"""

import ast
from typing import Iterable, List
import json
import numpy as np


def monomial_to_expvec(
    m: str, variables: Iterable[str] = ("x_1", "x_2", "x_3", "x_4")
) -> List[int]:
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
    return list(monomial_to_expvec(generator) for generator in ideal_str)


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
