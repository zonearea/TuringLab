"""Bölüm 2 ödev makineleri (TM-1 … TM-4)."""

from pathlib import Path

import pytest

from turinglab import SingleTapeTM

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def unary_to_binary() -> SingleTapeTM:
    return SingleTapeTM.from_yaml(ROOT / "machines" / "unary_to_binary.yaml")


@pytest.fixture(scope="module")
def binary_compare() -> SingleTapeTM:
    return SingleTapeTM.from_yaml(ROOT / "machines" / "binary_compare.yaml")


@pytest.fixture(scope="module")
def string_copy() -> SingleTapeTM:
    return SingleTapeTM.from_yaml(ROOT / "machines" / "string_copy.yaml")


@pytest.fixture(scope="module")
def unary_div3() -> SingleTapeTM:
    return SingleTapeTM.from_yaml(ROOT / "machines" / "unary_div3.yaml")


def test_unary_to_binary_loads(unary_to_binary: SingleTapeTM) -> None:
    assert unary_to_binary.name == "unary_to_binary"
    assert unary_to_binary.start_state == "q0"


@pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 16, 255])
def test_unary_to_binary_accept(unary_to_binary: SingleTapeTM, n: int) -> None:
    inp = "1" * n
    exp = bin(n)[2:]
    r = unary_to_binary.run(input_string=inp, max_steps=500_000, verbose=False)
    assert r.accepted is True
    assert r.reason == "accept"
    assert r.final_tape.strip("B") == exp


def test_unary_to_binary_empty_reject(unary_to_binary: SingleTapeTM) -> None:
    r = unary_to_binary.run(input_string="", max_steps=100, verbose=False)
    assert r.accepted is False
    assert r.reason == "reject"


def test_unary_to_binary_invalid_zero_reject(unary_to_binary: SingleTapeTM) -> None:
    r = unary_to_binary.run(input_string="0", max_steps=100, verbose=False)
    assert r.accepted is False
    assert r.reason == "reject"


def test_unary_to_binary_overflow_reject(unary_to_binary: SingleTapeTM) -> None:
    r = unary_to_binary.run(input_string="1" * 256, max_steps=500_000, verbose=False)
    assert r.accepted is False
    assert r.reason == "reject"


@pytest.mark.parametrize(
    ("inp", "accept"),
    [
        ("1100#1011", True),
        ("11#10", True),
        ("1011#1100", False),
        ("11#11", False),
        ("10#11", False),
    ],
)
def test_binary_compare_handbook(binary_compare: SingleTapeTM, inp: str, accept: bool) -> None:
    r = binary_compare.run(input_string=inp, max_steps=500_000, verbose=False)
    assert r.accepted is accept
    assert r.reason == ("accept" if accept else "reject")


@pytest.mark.parametrize(
    ("inp", "expected"),
    [
        ("abba", "abba#abba"),
        ("a", "a#a"),
        ("ab", "ab#ab"),
        ("abab", "abab#abab"),
    ],
)
def test_string_copy_output(string_copy: SingleTapeTM, inp: str, expected: str) -> None:
    r = string_copy.run(input_string=inp, max_steps=500_000, verbose=False)
    assert r.accepted is True
    assert r.final_tape.strip("B") == expected


def test_string_copy_empty_reject(string_copy: SingleTapeTM) -> None:
    r = string_copy.run(input_string="", max_steps=100, verbose=False)
    assert r.accepted is False


@pytest.mark.parametrize(
    ("inp", "accept"),
    [
        ("111", True),
        ("111111", True),
        ("11", False),
        ("1", False),
        ("", False),
    ],
)
def test_unary_div3_mod(unary_div3: SingleTapeTM, inp: str, accept: bool) -> None:
    r = unary_div3.run(input_string=inp, max_steps=50_000, verbose=False)
    assert r.accepted is accept
