def relazione(A, condizione):
    return {(x, y) for x in A for y in A if condizione(x, y)}


def simmetrica(R):
    return all((b, a) in R for a, b in R)


def somma_pari(x, y):
    return (x + y) % 2 == 0
