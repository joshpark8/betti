"""
Read ideals from Macaulay2 output and encode into matrices
"""

from typing import Iterable, List


def m2_to_str(powers: list[str], terms: list[str]):
    """
    Accepts a list of exponents and list of variables and merges the two into an easier format to work with

    :param powers: array of exponents aligned to terms
    :type powers: list
    :param terms: array of terms aligned to exponents
    :type terms: list
    :return ideal: list
    """
    # print(powers)
    # print(terms, end="\t --> \t")

    tmp_ideal = [""]
    generator_index = 0
    for i, term in enumerate(terms):
        # print(powers[i])
        if term != " ":
            if term == ",":
                generator_index += 1
                tmp_ideal.append("")
                continue
            tmp_ideal[generator_index] = tmp_ideal[generator_index] + terms[i]
        elif i < len(powers) and powers[i] != " " and powers[i] != "\n":
            # print("TERM   ", ideal[generator], end="\t")
            # print("POWER  ", powers[i])
            tmp_ideal[generator_index] = (
                tmp_ideal[generator_index] + "^" + powers[i] + "*"
            )

    # remove all closing parentheses
    tmp_ideal[-1] = tmp_ideal[-1].replace(")", "")

    # clean up trailing asterisks
    for i, generator in enumerate(tmp_ideal):
        if generator[-1] == "*":
            tmp_ideal[i] = generator[:-1]

    return tmp_ideal


def monomial_to_expvec(m: str, variables: Iterable[str] = ("x", "y", "z")) -> List[int]:
    """
    Takes in monomials and outputs vector of exponents
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


def str_to_matrix(ideal: list[str]):
    """
    takes in generators as list of monomials and converts to matrix

    :param ideal_str: Description
    :type ideal_str: str
    """
    return list(monomial_to_expvec(generator) for generator in ideal)


if __name__ == "__main__":
    n = 1
    # get ideals from m2
    fin = open("ideals/generated ideals/ideals_{n}.txt", "r", encoding="utf8")
    all_ideals = []
    for line in fin:
        ideal = m2_to_str(powers=list(line[7:-1]), terms=list(fin.readline()[7:-2]))
        print(ideal)
        print(str_to_matrix(ideal), end="\n\n")
        all_ideals.append(ideal)

    # write cleaned ideals as text file
    fout = open(f"ideals/cleaned ideals/cleaned_ideals_{n}.txt", "a", encoding="utf8")
    fout.write(str(all_ideals))
