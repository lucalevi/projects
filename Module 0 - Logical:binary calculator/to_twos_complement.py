from decimal_to_base import decimal_to_base
from base_to_decimal import base_to_decimal


def to_twos_complement(n, bits=8):
    minimo, massimo = -(2 ** (bits - 1)), 2 ** (bits - 1) - 1
    if not (minimo <= n <= massimo):
        raise ValueError(
            f"{n} non rappresentabile con {bits} bit (range {minimo}..{massimo})"
        )
    if n >= 0:
        return decimal_to_base(n, 2).zfill(bits)
    return decimal_to_base(n + 2**bits, 2)


def from_twos_complement(s):
    bits = len(s)
    bit_di_segno = s[0]
    resto = s[1:]

    valore_segno = -(2 ** (bits - 1)) if bit_di_segno == "1" else 0
    valore_resto = base_to_decimal(resto, 2)

    return valore_segno + valore_resto


def add_twos_complement(a, b, bits=8):
    n1 = from_twos_complement(a)
    n2 = from_twos_complement(b)
    risultato = n1 + n2

    minimo, massimo = -(2 ** (bits - 1)), 2 ** (bits - 1) - 1
    overflow = not (minimo <= risultato <= massimo)

    if overflow:
        return None, True  # o solleva un'eccezione, decidiamo dopo
    return to_twos_complement(risultato, bits), False


if __name__ == "__main__":
    assert to_twos_complement(0) == "00000000"
    assert to_twos_complement(1) == "00000001"
    assert to_twos_complement(127) == "01111111"
    assert to_twos_complement(-1) == "11111111"
    assert to_twos_complement(-20) == "11101100"  # il tuo esempio a mano
    assert to_twos_complement(-128) == "10000000"  # il caso limite
    for n in [200, -129]:
        try:
            to_twos_complement(n)
            assert False, "doveva sollevare ValueError"
        except ValueError:
            pass

    assert from_twos_complement("00000000") == 0
    assert from_twos_complement("00000001") == 1
    assert from_twos_complement("01111111") == 127
    assert from_twos_complement("11111111") == -1
    assert from_twos_complement("11101100") == -20
    assert from_twos_complement("10000000") == -128

    for n in range(-128, 128):
        assert from_twos_complement(to_twos_complement(n)) == n

    minimo, massimo = -128, 127
    for n1 in range(minimo, massimo + 1):
        for n2 in range(minimo, massimo + 1):
            vero_risultato = n1 + n2
            risultato, overflow = add_twos_complement(
                to_twos_complement(n1), to_twos_complement(n2)
            )
            if minimo <= vero_risultato <= massimo:
                assert overflow == False
                assert from_twos_complement(risultato) == vero_risultato
            else:
                assert overflow == True
                assert risultato is None

    print("Tutti i test passati")
