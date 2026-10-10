def relazione(A, condizione):
    return {(x, y) for x in A for y in A if condizione(x, y)}


def minore(x, y):
    return x < y


def divide(x, y):
    return y % x == 0


print(relazione({1, 2, 3}, minore))
print(relazione({1, 2, 3, 4, 5, 6}, divide))
