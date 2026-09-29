digits = "0123456789ABCDEF"


def _decimal_to_base_helper(n, base):
    if n == 0:
        return ""
    return _decimal_to_base_helper(n // base, base) + digits[n % base]


def decimal_to_base(n, base):
    if n == 0:
        return "0"
    return _decimal_to_base_helper(n, base)


if __name__ == "__main__":
    for n in [0, 1, 2, 13, 255, 4096]:
        assert decimal_to_base(n, 2) == bin(n)[2:]
        assert decimal_to_base(n, 16) == hex(n)[2:].upper()
    print("Tutti i test passati")

    print(_decimal_to_base_helper(0, 2))
