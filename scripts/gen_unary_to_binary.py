#!/usr/bin/env python3
"""unary_to_binary.yaml — X sonrası K=8 bit (MSB sol), n<=255."""

from pathlib import Path

B = "B"
X = "X"
K = 8


def t(rows: list, q: str, r: str, nq: str, w: str, m: str) -> None:
    rows.append({"state": q, "read": r, "next": nq, "write": w, "move": m})


def chain_r(rows: list, q0: str, q_end: str, n: int) -> None:
    cur = q0
    for i in range(n - 1):
        nxt = f"x{i}"
        for s in ("0", "1", B, X):
            t(rows, cur, s, nxt, s, "R")
        cur = nxt
    for s in ("0", "1", B, X):
        t(rows, cur, s, q_end, s, "R")


def main() -> None:
    rows: list = []

    t(rows, "q0", B, "q_reject", B, "R")
    t(rows, "q0", "1", "q1r", "1", "R")
    t(rows, "q1r", B, "q1l", B, "L")
    t(rows, "q1l", "1", "q_accept", "1", "R")
    t(rows, "q1r", "1", "q_sc", "1", "R")
    t(rows, "q_sc", "1", "q_sc", "1", "R")
    t(rows, "q_sc", B, "q_wx", X, "L")
    t(rows, "q_wx", "1", "q_wl", "1", "L")
    t(rows, "q_wl", "1", "q_wl", "1", "L")
    t(rows, "q_wl", B, "q_fl", B, "R")

    t(rows, "q_fl", "1", "q_er", B, "R")
    t(rows, "q_er", "1", "q_er", "1", "R")
    t(rows, "q_er", B, "q_er", B, "R")
    t(rows, "q_er", X, "q_msb", X, "R")

    chain_r(rows, "q_msb", "q_lsb", K - 1)

    t(rows, "q_lsb", B, "q_rw1", "1", "L")
    t(rows, "q_lsb", "0", "q_rw1", "1", "L")
    t(rows, "q_lsb", "1", "ca0", "0", "L")

    for j in range(K - 2):
        nxt = f"ca{j + 1}"
        t(rows, f"ca{j}", "0", "q_rw1", "1", "L")
        t(rows, f"ca{j}", "1", nxt, "0", "L")
        t(rows, f"ca{j}", B, "q_rw1", "1", "L")

    t(rows, "ca6", "0", "q_rw1", "1", "L")
    t(rows, "ca6", "1", "q_ov", "0", "L")
    t(rows, "ca6", B, "q_rw1", "1", "L")

    t(rows, "q_ov", X, "q_rv", X, "R")
    for s in ("0", "1"):
        t(rows, "q_rv", s, "q_rv", s, "R")
    t(rows, "q_rv", B, "q_reject", B, "R")

    for s in ("0", "1", B):
        t(rows, "q_rw1", s, "q_rw1", s, "L")
    t(rows, "q_rw1", X, "q_lf", X, "L")

    t(rows, "q_lf", "1", "q_lf", "1", "L")
    t(rows, "q_lf", B, "q_lr", B, "R")
    t(rows, "q_lr", B, "q_lr", B, "R")
    t(rows, "q_lr", "1", "q_er", B, "R")
    t(rows, "q_lr", X, "q_cx", B, "R")

    t(rows, "q_cx", "0", "q_cz", B, "R")
    t(rows, "q_cx", "1", "q_accept", "1", "R")
    t(rows, "q_cx", B, "q_accept", B, "R")
    t(rows, "q_cz", "0", "q_cz", B, "R")
    t(rows, "q_cz", "1", "q_accept", "1", "R")
    t(rows, "q_cz", B, "q_accept", B, "R")

    states = {tr["state"] for tr in rows} | {tr["next"] for tr in rows}
    sl = sorted(states)
    lines = [
        'name: "unary_to_binary"',
        'description: "Unary 1^n sayisini ikili yazima cevirir (ornek: 111 -> 11)."',
        "states: [" + ", ".join(sl) + "]",
        'input_alphabet: ["0", "1"]',
        'tape_alphabet: ["0", "1", "B", "X"]',
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

    out = Path(__file__).resolve().parents[1] / "machines" / "unary_to_binary.yaml"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("transitions", len(rows))


if __name__ == "__main__":
    main()
