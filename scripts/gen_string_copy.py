#!/usr/bin/env python3
"""string_copy.yaml — w -> w#w (alfabe a,b; isaret X)."""

from pathlib import Path

B = "B"
H = "#"
X = "X"


def t(rows: list, q: str, r: str, nq: str, w: str, m: str) -> None:
    rows.append({"state": q, "read": r, "next": nq, "write": w, "move": m})


def main() -> None:
    rows: list = []

    t(rows, "q0", B, "q_reject", B, "R")
    t(rows, "q0", H, "q_reject", H, "R")
    t(rows, "q0", X, "q_reject", X, "R")
    for c in ("a", "b"):
        t(rows, "q0", c, "q_run", c, "R")

    for c in ("a", "b", X):
        t(rows, "q_run", c, "q_run", c, "R")
    t(rows, "q_run", B, "q_home", H, "L")
    t(rows, "q_run", H, "q_reject", H, "R")

    for c in ("a", "b", H, X):
        t(rows, "q_home", c, "q_home", c, "L")
    t(rows, "q_home", B, "q_loop", B, "R")

    t(rows, "q_loop", "a", "q_mka", X, "R")
    t(rows, "q_loop", "b", "q_mkb", X, "R")
    t(rows, "q_loop", X, "q_loop", X, "R")
    t(rows, "q_loop", H, "q_done", H, "L")
    t(rows, "q_loop", B, "q_reject", B, "R")

    for c in ("a", "b", X):
        t(rows, "q_mka", c, "q_mka", c, "R")
        t(rows, "q_mkb", c, "q_mkb", c, "R")
    t(rows, "q_mka", H, "q_tenda", H, "R")
    t(rows, "q_mkb", H, "q_tendb", H, "R")
    t(rows, "q_mka", B, "q_reject", B, "R")
    t(rows, "q_mkb", B, "q_reject", B, "R")

    for c in ("a", "b", X):
        t(rows, "q_tenda", c, "q_tenda", c, "R")
        t(rows, "q_tendb", c, "q_tendb", c, "R")
    t(rows, "q_tenda", H, "q_tenda", H, "R")
    t(rows, "q_tendb", H, "q_tendb", H, "R")
    t(rows, "q_tenda", B, "q_wa", B, "L")
    t(rows, "q_tendb", B, "q_wb", B, "L")

    for c in ("a", "b", H):
        t(rows, "q_wa", c, "q_wa", c, "L")
    t(rows, "q_wa", X, "q_puta", X, "R")
    t(rows, "q_wa", B, "q_reject", B, "R")

    for c in ("a", "b", H):
        t(rows, "q_wb", c, "q_wb", c, "L")
    t(rows, "q_wb", X, "q_putb", X, "R")
    t(rows, "q_wb", B, "q_reject", B, "R")

    for c in ("a", "b", H, X):
        t(rows, "q_puta", c, "q_puta", c, "R")
        t(rows, "q_putb", c, "q_putb", c, "R")
    t(rows, "q_puta", B, "q_reta", "a", "L")
    t(rows, "q_putb", B, "q_retb", "b", "L")

    for c in ("a", "b", H):
        t(rows, "q_reta", c, "q_reta", c, "L")
        t(rows, "q_retb", c, "q_retb", c, "L")
    t(rows, "q_reta", X, "q_loop", "a", "R")
    t(rows, "q_retb", X, "q_loop", "b", "R")
    t(rows, "q_reta", B, "q_reject", B, "R")
    t(rows, "q_retb", B, "q_reject", B, "R")

    t(rows, "q_done", X, "q_done", X, "L")
    for c in ("a", "b", H):
        t(rows, "q_done", c, "q_done", c, "L")
    t(rows, "q_done", B, "q_accept", B, "R")

    states = {tr["state"] for tr in rows} | {tr["next"] for tr in rows}
    lines = [
        'name: "string_copy"',
        'description: "w -> w#w kopya (ornek: abba -> abba#abba)."',
        "states: [" + ", ".join(sorted(states)) + "]",
        'input_alphabet: ["a", "b"]',
        'tape_alphabet: ["a", "b", "#", "B", "X"]',
        'blank: "B"',
        "start_state: q0",
        "accept_states: [q_accept]",
        "reject_states: [q_reject]",
        "transitions:",
    ]
    for tr in rows:
        lines.append(
            f'  - {{state: {tr["state"]}, read: "{tr["read"]}", next: {tr["next"]}, '
            f'write: "{tr["write"]}", move: {tr["move"]}}}'
        )

    out = Path(__file__).resolve().parents[1] / "machines" / "string_copy.yaml"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("transitions", len(rows))


if __name__ == "__main__":
    main()
