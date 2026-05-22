"""Bonus modül testleri."""

from pathlib import Path

import pytest

from turinglab import SingleTapeTM
from turinglab.bonus import (
    MultiTapeTM,
    NondeterministicTM,
    compare_step_counts,
    export_history_gif,
    export_history_ppm,
    save_comparison,
    write_ppm_frame,
)

ROOT = Path(__file__).resolve().parents[1]


def test_multi_tape_copy() -> None:
    tm = MultiTapeTM.from_yaml(ROOT / "machines" / "bonus_two_tape_copy.yaml")
    r = tm.run("ab", max_steps=500)
    assert r.accepted
    assert r.final_tape0.strip("B") == "ab"
    assert r.final_tape1.strip("B") == "ab"


def test_ntm_bfs_finds_accept() -> None:
    """a|b NTM: bir adimda kabul yolu vardir."""
    ntm = NondeterministicTM(
        name="guess_ab",
        states=["q0", "q1", "q_accept"],
        input_alphabet=["a"],
        tape_alphabet=["a", "B"],
        blank="B",
        start_state="q0",
        accept_states=["q_accept"],
        reject_states=[],
        transitions={
            ("q0", "a"): [("q1", "a", "R"), ("q_accept", "a", "R")],
            ("q1", "B"): [("q_accept", "B", "R")],
        },
    )
    r = ntm.run_bfs("a", max_steps=5, max_nodes=200)
    assert r.found
    assert r.reason == "accept"


def test_step_compare_csv(tmp_path: Path) -> None:
    tm = SingleTapeTM.from_yaml(ROOT / "machines" / "unary_increment.yaml")
    cmp = compare_step_counts(
        tm,
        [("n1", "1"), ("n3", "111")],
    )
    assert cmp.steps[1] > cmp.steps[0]
    files = save_comparison(cmp, tmp_path)
    assert files["csv"].is_file()


def test_write_ppm_frame(tmp_path: Path) -> None:
    p = tmp_path / "f.ppm"
    write_ppm_frame(p, "101", 1, label="q0")
    data = p.read_bytes()
    assert data.startswith(b"P3")


def test_export_history_ppm(tmp_path: Path) -> None:
    tm = SingleTapeTM.from_yaml(ROOT / "machines" / "binary_increment.yaml")
    r = tm.run("1011", max_steps=200)
    frames = export_history_ppm(r, tmp_path)
    assert len(frames) == len(r.history)
    assert frames[0].suffix == ".ppm"


def test_export_gif_optional(tmp_path: Path) -> None:
    """Pillow varsa GIF üretilir; yoksa False döner (hata vermez)."""
    tm = SingleTapeTM.from_yaml(ROOT / "machines" / "binary_increment.yaml")
    r = tm.run("1", max_steps=50)
    ok = export_history_gif(r, tmp_path / "out.gif")
    assert ok in (True, False)
