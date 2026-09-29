# Module 0 - Logical/binary calculator

Phase 0 of the course ("How a computer thinks"): small, dependency-free Python building blocks for a command-line binary/logic calculator. The code covers how numbers are represented in different bases and in two's complement, and how a boolean expression can be parsed and evaluated.

## Contents

| File | Syllabus | What it does |
|------|----------|--------------|
| `decimal_to_base.py` | 0.1 | Converts a non-negative integer to a string in any base from 2 to 16 (repeated division) |
| `base_to_decimal.py` | 0.1 | Converts a string in base 2-16 back to an integer (Horner's method) with digit validation |
| `to_twos_complement.py` | 0.1 | Encodes/decodes signed integers in two's complement and adds them with overflow detection |
| `decimal_to_base_recursive.py` | 0.3 | Same conversion as `decimal_to_base.py`, written recursively |
| [`../tokenizer.py`](../tokenizer.py) | 0.2 | Tokenizer, stack-based evaluator and truth-table generator for boolean expressions |

## How it works

### Base conversion

`decimal_to_base(n, base)` repeatedly divides by the base and collects the remainders, most significant digit last. `base_to_decimal(s, base)` does the inverse with `result = result * base + digit`, and raises `ValueError` if a digit is not valid for the base.

```python
>>> decimal_to_base(255, 16)
'FF'
>>> base_to_decimal("1101", 2)
13
```

`decimal_to_base_recursive.py` expresses the same idea as recursion: the representation of `n` is the representation of `n // base` followed by the digit `n % base`, with `n == 0` as the base case.

### Two's complement

- `to_twos_complement(n, bits=8)` encodes `n` in `bits` bits. Negative numbers are encoded as the binary form of `n + 2**bits`. It raises `ValueError` if `n` is outside the representable range (-128..127 for 8 bits).
- `from_twos_complement(s)` decodes a bit string: the sign bit has weight `-2**(bits-1)`, and the remaining bits are read as an ordinary unsigned number.
- `add_twos_complement(a, b, bits=8)` returns `(result, overflow)`. On overflow it returns `(None, True)`.

```python
>>> to_twos_complement(-20)
'11101100'
>>> from_twos_complement("10000000")
-128
>>> add_twos_complement("01111111", "00000001")   # 127 + 1
(None, True)
```

The adder decodes both operands, adds them as integers, checks the range and re-encodes the result. It is not a bit-level adder built from logic gates.

### Boolean expressions

`tokenizer.py` handles fully parenthesised expressions with `AND`, `OR` and `NOT`.

1. `tokenize` pads parentheses with spaces and splits on whitespace.
2. `get_variables` collects the variable names in order of first appearance.
3. `evaluate` runs a single pass over the tokens with a stack. A closing parenthesis pops the right operand, the operator and the left operand, and pushes the result. A `NOT` is resolved as soon as a value lands on top of it.
4. `truth_table` evaluates the expression for every combination of `True`/`False` (via `itertools.product`) and prints the table.

```
>>> truth_table("((A OR B) AND (NOT (A AND B)))")   # exclusive or
A B RISULTATO
V V -> F
V F -> V
F V -> V
F F -> F
```

## Running

The scripts import each other, so run them from inside this folder. Each one runs its tests when executed directly and prints `Tutti i test passati` ("all tests passed"):

```bash
python decimal_to_base.py
python base_to_decimal.py
python to_twos_complement.py
python decimal_to_base_recursive.py
python ../tokenizer.py     # also prints three sample truth tables
```

Checked with Python 3.10.

## How the code is tested

- Base conversion is compared against Python's built-ins (`bin`, `hex`, `int(s, base)`).
- Round trips: `base_to_decimal(decimal_to_base(n, b), b) == n` for every `n < 1000` and every base from 2 to 16.
- Two's complement: all 256 eight-bit values survive an encode/decode round trip, and addition is checked against ordinary integer addition for all 65,536 pairs of 8-bit operands, including the overflow cases.
- The evaluator is checked against Python's own `and`/`or`/`not` for every assignment of a sample expression. It must reject an expression that is not fully parenthesised.

## Known limitations

- Base conversion supports non-negative integers only, with digits `0-9A-F`. `decimal_to_base_recursive.py` does not validate the base.
- The tokenizer relies on whitespace and parentheses, so `(AANDB)` is read as a single variable name. Operators must be uppercase and cannot be used as variable names.
- There is no operator precedence: every binary operation must be wrapped in its own parentheses, so `(A AND B) OR NOT C` raises `ValueError` while `((A AND B) OR NOT C)` works.
- This folder has no code yet for floating point (IEEE 754) or text encodings (ASCII/Unicode), and no command-line entry point that ties the pieces together.
