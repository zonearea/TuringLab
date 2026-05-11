"""TM motoru testleri (Bölüm 1)."""

from pathlib import Path

import pytest

from turinglab import RunResult, SingleTapeTM

ROOT = Path(__file__).resolve().parents[1]


def test_from_yaml_loads_binary_increment() -> None:
    path = ROOT / "machines" / "binary_increment.yaml"
    tm = SingleTapeTM.from_yaml(path)
    assert tm.name == "binary_increment"
    assert tm.start_state == "q0"


def test_binary_increment_handbook_example() -> None:
    tm = SingleTapeTM.from_yaml(ROOT / "machines" / "binary_increment.yaml")
    result: RunResult = tm.run(input_string="1011", max_steps=1000, verbose=False)
    assert result.accepted is True
    assert result.reason == "accept"
    assert result.final_tape.strip("B") == "1100"
    assert result.steps >= 1
    assert len(result.history) == result.steps + 1


def test_no_transition() -> None:
    yaml_text = """
name: "halt_no_move"
states: [q0]
input_alphabet: ["0"]
tape_alphabet: ["0", "B"]
blank: "B"
start_state: q0
accept_states: []
reject_states: []
transitions: []
"""
    import tempfile

    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8") as f:
        f.write(yaml_text)
        p = f.name
    try:
        tm = SingleTapeTM.from_yaml(p)
        r = tm.run("0", max_steps=10)
        assert r.accepted is False
        assert r.reason == "no_transition"
        assert r.steps == 0
    finally:
        Path(p).unlink(missing_ok=True)


def test_timeout() -> None:
    yaml_text = """
name: "infinite_right"
states: [q0]
input_alphabet: ["0"]
tape_alphabet: ["0", "B"]
blank: "B"
start_state: q0
accept_states: []
reject_states: []
transitions:
  - {state: q0, read: "0", next: q0, write: "0", move: R}
  - {state: q0, read: "B", next: q0, write: "B", move: R}
"""
    import tempfile

    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8") as f:
        f.write(yaml_text)
        p = f.name
    try:
        tm = SingleTapeTM.from_yaml(p)
        r = tm.run("0", max_steps=5)
        assert r.accepted is False
        assert r.reason == "timeout"
        assert r.steps == 5
    finally:
        Path(p).unlink(missing_ok=True)


def test_invalid_yaml_missing_field() -> None:
    import tempfile

    bad = "name: x\nstates: []\n"
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8") as f:
        f.write(bad)
        p = f.name
    try:
        with pytest.raises(ValueError, match="Eksik alan"):
            SingleTapeTM.from_yaml(p)
    finally:
        Path(p).unlink(missing_ok=True)


def test_verbose_contains_bracket_head(capsys: pytest.CaptureFixture[str]) -> None:
    tm = SingleTapeTM.from_yaml(ROOT / "machines" / "binary_increment.yaml")
    tm.run(input_string="1", max_steps=50, verbose=True)
    out = capsys.readouterr().out
    assert "[" in out and "]" in out
    assert "Adım 0" in out
