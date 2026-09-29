from decimal_to_base import decimal_to_base


def base_to_decimal(s, base):
    digits = "0123456789ABCDEF"
    result = 0
    for digit in s:
        valore = digits.index(digit.upper())

        if valore >= base:
            raise ValueError(f"Cifra {digit!r} non valida in base {base}")

        result = result * base + valore
    return result


if __name__ == "__main__":
    casi = [
        ("0", 2),
        ("1", 2),
        ("1101", 2),
        ("11111111", 2),
        ("326", 8),
        ("FF", 16),
        ("1000", 16),
        ("ff".upper(), 16),
    ]
    for s, base in casi:
        assert base_to_decimal(s, base) == int(s, base)
    for n in range(1000):
        for base in range(2, 17):
            assert base_to_decimal(decimal_to_base(n, base), base) == n
    print("Tutti i test passati")
