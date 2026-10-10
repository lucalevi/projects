def riflessiva(R, A):
    return all((x, x) in R for x in A)


def minore(x, y):
    return x < y


def divide(x, y):
    return y % x == 0


def relazione(A, condizione):
    return {(x, y) for x in A for y in A if condizione(x, y)}


A = {1, 2, 3, 4, 5, 6}
D = relazione(A, divide)
M = relazione(A, minore)

print(riflessiva(D, A))
print(riflessiva(M, A))
print(len(D), len(M))
