from itertools import product


def tokenize(expression):
    expression = expression.replace("(", " ( ").replace(")", " ) ")
    return expression.split()


def resolve_nots(stack):
    while len(stack) >= 2 and stack[-2] == "NOT":
        value = stack.pop()
        stack.pop()  # scarta il NOT
        stack.append(not value)


def evaluate(tokens, values):
    stack = []
    for token in tokens:
        if token in ("(", "AND", "OR", "NOT"):
            stack.append(token)
        elif token == ")":
            b = stack.pop()
            if stack[-1] == "(":
                stack.pop()  # parentesi con un solo valore
                res = b
            else:
                op = stack.pop()
                a = stack.pop()
                stack.pop()  # scarta "("
                res = (a and b) if op == "AND" else (a or b)
            stack.append(res)
            resolve_nots(stack)

        else:
            stack.append(values[token])
            resolve_nots(stack)

    if len(stack) != 1:
        raise ValueError("espressione non valida")
    return stack[0]


def get_variables(tokens):
    variables = []
    SPECIAL = {"(", ")", "AND", "OR", "NOT"}
    for token in tokens:
        if token not in SPECIAL and token not in variables:
            variables.append(token)
    return variables


def truth_table(expression):
    tokens = tokenize(expression)
    variables = get_variables(tokens)

    print(" ".join(variables), "RISULTATO")

    for combinazione in product([True, False], repeat=len(variables)):
        values = dict(zip(variables, combinazione))
        result = evaluate(tokens, values)

        riga = " ".join("V" if valore else "F" for valore in combinazione)
        print(riga, "->", "V" if result else "F")


if __name__ == "__main__":
    assert tokenize("A AND B") == ["A", "AND", "B"]
    assert tokenize("  A   AND B  ") == ["A", "AND", "B"]
    assert tokenize("(AANDB)") == ["(", "AANDB", ")"]  # limite noto, non un bug

    tokens = tokenize("((A AND B) OR NOT C)")
    for a, b, c in product([True, False], repeat=3):
        atteso = (a and b) or (not c)
        assert evaluate(tokens, {"A": a, "B": b, "C": c}) == atteso

    try:
        evaluate(tokenize("(A AND B) OR NOT C"), {"A": True, "B": True, "C": True})
        assert False, "doveva sollevare ValueError"
    except ValueError:
        pass

    assert get_variables(tokenize("((A AND B) OR NOT C)")) == ["A", "B", "C"]
    assert get_variables(tokenize("(A AND A)")) == ["A"]
    assert get_variables(tokenize("(NOT B)")) == ["B"]

    truth_table("((A AND B) OR NOT C)")
    truth_table("(NOT (A AND B))")
    truth_table("((A OR B) AND (NOT (A AND B)))")

    print("Tutti i test passati")
