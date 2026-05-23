#!/usr/bin/env python3
"""Bonus modül terminal demoları.

Kullanım:
  python scripts/demo_bonus.py bonus1
  python scripts/demo_bonus.py bonus2
  python scripts/demo_bonus.py bonus2 --girdi a
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from turinglab.bonus import MultiTapeTM, NondeterministicTM  # noqa: E402


def _utf8() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:
                pass


def _banner(title: str) -> None:
    line = "=" * 60
    print(f"\n{line}\n  {title}\n{line}\n")


def demo_multi_tape(girdi: str) -> None:
    path = ROOT / "machines" / "bonus_two_tape_copy.yaml"
    tm = MultiTapeTM.from_yaml(path)
    _banner("Bonus 1 — Çok şeritli TM (bonus_two_tape_copy)")
    print(f"Dosya : machines/bonus_two_tape_copy.yaml")
    print(f"Girdi : {girdi!r}\n")
    print("--- Adımlar (T0 = şerit 0, T1 = şerit 1) ---\n")
    r = tm.run(girdi, max_steps=50_000, verbose=True)
    print(
        f"\n>>> Sonuç: {r.reason} | T0: {r.final_tape0!r} | T1: {r.final_tape1!r} | adım: {r.steps}\n"
    )


def _demo_ntm() -> NondeterministicTM:
    """Testteki küçük NTM: q0'da 'a' okununca iki seçenek (tahmin)."""
    return NondeterministicTM(
        name="guess_a_accept",
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


def demo_ntm_bfs(girdi: str) -> None:
    ntm = _demo_ntm()
    _banner("Bonus 2 — Belirsiz TM + BFS")
    print("Makine : tek şeritli NTM (kod içinde tanımlı demo)")
    print(f"Girdi  : {girdi!r}\n")
    print("Belirsiz geçişler (aynı durum+sembol → birden fazla seçenek):")
    print("  q0, 'a' okuyunca → (1) q1'e git  VEYA  (2) doğrudan q_accept")
    print("  q1, boşluk okuyunca → q_accept\n")
    print("BFS: tüm olası yolları katman katman dener, ilk kabul yolunu bulur.\n")
    r = ntm.run_bfs(girdi, max_steps=10, max_nodes=500)
    if r.found and r.history:
        print("--- Bulunan kabul yolu ---\n")
        for i, step in enumerate(r.history):
            print(f"  Adım {i} | {step.state} | şerit: {step.tape!r} | kafa: {step.head_position}")
    print(
        f"\n>>> Sonuç: {r.reason} | yol uzunluğu: {r.steps} adım | "
        f"incelenen yapılandırma: {r.paths_explored}\n"
    )


def main() -> None:
    _utf8()
    p = argparse.ArgumentParser(description="TuringLab bonus demoları")
    p.add_argument(
        "demo",
        choices=("multi_tape", "bonus1", "ntm", "bonus2"),
        help="bonus1=çok şerit, bonus2=NTM+BFS",
    )
    p.add_argument("--girdi", default=None, help="Girdi (bonus1: ab, bonus2: a)")
    args = p.parse_args()

    if args.demo in ("multi_tape", "bonus1"):
        demo_multi_tape(args.girdi or "ab")
    else:
        demo_ntm_bfs(args.girdi or "a")


if __name__ == "__main__":
    main()
