def decimal_to_base(n, base):
    if base < 2 or base > 16:
        raise ValueError("La base dev'essere compresa tra 2 e 16.")

    if n == 0:
        return "0"

    digits = "0123456789ABCDEF"
    converted_number = ""
    while n > 0:
        remainder = n % base
        digit = digits[remainder]
        n = n // base

        converted_number = digit + converted_number

    return converted_number


if __name__ == "__main__":
    for n in [0, 1, 2, 13, 255, 4096]:
        assert decimal_to_base(n, 2) == bin(n)[2:]
        assert decimal_to_base(n, 16) == hex(n)[2:].upper()
    print("Tutti i test passati")
