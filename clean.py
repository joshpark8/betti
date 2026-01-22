"""
Read ideals from Macaulay2 output and encode into matrices
"""

import ast
from typing import Iterable, List
import json
from sklearn.ensemble import RandomForestClassifier


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
    return list(monomial_to_expvec(generator) for generator in ideal_str)


def brace_string_to_list(s: str):
    """
    Converts "{{1, 0}, {0, 0}, ...}" -> [[1, 0], [0, 0], ...]

    :param s: betti table in string format
    :type s: str
    """
    t = s.strip().replace("{", "[").replace("}", "]")
    return ast.literal_eval(t)


if __name__ == "__main__":
    FILEPATH = "generated/ideals.json"
    try:
        with open(FILEPATH, "r", encoding="utf8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{FILEPATH}' was not found.")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON from {FILEPATH}: {e}")

    cleaned = dict()
    for key in data:
        generators = key[6:-1].split(",")
        print(key[6:-1])
        print(str_to_matrix(generators))

        betti = data[key][7:]
        print(brace_string_to_list(betti))