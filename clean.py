"""
Docstring for clean
"""


def clean_ideal(powers: list, terms: list):
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


if __name__ == "__main__":

    file_in = open("ideals/generated ideals/ideals_1.txt", "r", encoding="utf8")
    all_ideals = []
    for line in file_in:
        ideal = clean_ideal(powers=line[7:-1], terms=file_in.readline()[7:-2])
        print(ideal, end="\n\n")
        all_ideals.append(ideal)

    file_out = open("ideals/cleaned ideals/cleaned_ideals_1.txt", "a", encoding="utf8")
    file_out.write(str(all_ideals))
