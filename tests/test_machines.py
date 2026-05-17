"""Örnek makine YAML’ları (Bölüm 2 — TM-1 unary→binary)."""

from pathlib import Path

import pytest

from turinglab import SingleTapeTM

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def unary_to_binary() -> SingleTapeTM:
    return SingleTapeTM.from_yaml(ROOT / "machines" / "unary_to_binary.yaml")


def test_unary_to_binary_loads(unary_to_binary: SingleTapeTM) -> None:
    assert unary_to_binary.name == "unary_to_binary"
    assert unary_to_binary.start_state == "q0"


@pytest.mark.parametrize(
    "n",
    [1, 2, 3, 4, 5, 16, 255],
)
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
    """K=8 bit alan: n>255 taşma yolu q_rv → q_reject."""
    r = unary_to_binary.run(input_string="1" * 256, max_steps=500_000, verbose=False)
    assert r.accepted is False
    assert r.reason == "reject"
