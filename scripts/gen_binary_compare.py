#!/usr/bin/env python3
"""binary_compare.yaml — sol > sag; karsilastirilan bitler x0/x1 ile isaretlenir."""

from pathlib import Path

HASH = "#"
BLANK = "B"


def t(rows: list, q: str, r: str, nq: str, w: str, m: str) -> None:
    rows.append({"state": q, "read": r, "next": nq, "write": w, "move": m})


def main() -> None:
    rows: list = []

    t(rows, "q0", BLANK, "q_reject", BLANK, "R")
    t(rows, "q0", HASH, "q_reject", HASH, "R")
    for s in ("r", "s"):
        t(rows, "q0", s, "q_reject", s, "R")
    for s in ("0", "1"):
        t(rows, "q0", s, "q_scan", s, "R")

    for s in ("0", "1", "r", "s"):
        t(rows, "q_scan", s, "q_scan", s, "R")
    t(rows, "q_scan", HASH, "q_back", HASH, "L")
    t(rows, "q_scan", BLANK, "q_reject", BLANK, "R")

    for s in ("0", "1", HASH, "r", "s"):
        t(rows, "q_back", s, "q_back", s, "L")
    t(rows, "q_back", BLANK, "q_next", BLANK, "R")

    for s in ("r", "s"):
        t(rows, "q_next", s, "q_next", s, "R")
    t(rows, "q_next", BLANK, "q_next", BLANK, "R")
    t(rows, "q_next", "0", "q_g0", "r", "R")
    t(rows, "q_next", "1", "q_g1", "s", "R")
    t(rows, "q_next", HASH, "q_left_done", HASH, "R")

    for s in ("0", "1", "r", "s"):
        t(rows, "q_g0", s, "q_g0", s, "R")
    t(rows, "q_g0", HASH, "q_r0", HASH, "R")
    t(rows, "q_g0", BLANK, "q_reject", BLANK, "R")

    for s in ("0", "1", "r", "s"):
        t(rows, "q_g1", s, "q_g1", s, "R")
    t(rows, "q_g1", HASH, "q_r1", HASH, "R")
    t(rows, "q_g1", BLANK, "q_reject", BLANK, "R")

    for s in ("r", "s"):
        t(rows, "q_r0", s, "q_r0", s, "R")
    t(rows, "q_r0", "0", "q_backl", "r", "L")
    t(rows, "q_r0", "1", "q_reject", "1", "R")
    t(rows, "q_r0", HASH, "q_reject", HASH, "R")
    t(rows, "q_r0", BLANK, "q_reject", BLANK, "R")

    for s in ("r", "s"):
        t(rows, "q_r1", s, "q_r1", s, "R")
    t(rows, "q_r1", "0", "q_accept", "0", "R")
    t(rows, "q_r1", "1", "q_backl", "s", "L")
    t(rows, "q_r1", HASH, "q_reject", HASH, "R")
    t(rows, "q_r1", BLANK, "q_reject", BLANK, "R")

    for s in ("0", "1", "r", "s", HASH):
        t(rows, "q_backl", s, "q_backl", s, "L")
    t(rows, "q_backl", BLANK, "q_prevl", BLANK, "L")

    for s in ("r", "s", HASH):
        t(rows, "q_prevl", s, "q_prevl", s, "L")
    t(rows, "q_prevl", "0", "q_next", "0", "R")
    t(rows, "q_prevl", "1", "q_next", "1", "R")
    t(rows, "q_prevl", BLANK, "q_next", BLANK, "R")

    for s in ("r", "s"):
        t(rows, "q_left_done", s, "q_left_done", s, "R")
    t(rows, "q_left_done", "0", "q_reject", "0", "R")
    t(rows, "q_left_done", "1", "q_accept", "1", "R")
    t(rows, "q_left_done", HASH, "q_reject", HASH, "R")
    t(rows, "q_left_done", BLANK, "q_reject", BLANK, "R")

    states = {tr["state"] for tr in rows} | {tr["next"] for tr in rows}
    lines = [
        'name: "binary_compare"',
        'description: "Sol ikili > sag ikili ise kabul (ornek: 1100#1011)."',
        "states: [" + ", ".join(sorted(states)) + "]",
        'input_alphabet: ["0", "1", "#"]',
        'tape_alphabet: ["0", "1", "#", "B", "r", "s"]',
        'blank: "B"',
        "start_state: q0",
        "accept_states: [q_accept]",
        "reject_states: [q_reject]",
        "transitions:",
    ]
    for tr in rows:
        lines.append(
            f'  - {{state: {tr["state"]}, read: "{tr["read"]}", next: {tr["next"]}, write: "{tr["write"]}", move: {tr["move"]}}}'
        )

    out = Path(__file__).resolve().parents[1] / "machines" / "binary_compare.yaml"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("transitions", len(rows))


if __name__ == "__main__":
    main()
