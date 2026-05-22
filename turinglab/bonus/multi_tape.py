"""İki şeritli deterministik Turing makinesi (bonus)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Mapping, Tuple

import yaml

from turinglab.tm_engine import _as_str_list, _strip_blanks

Move = str


@dataclass(frozen=True)
class MultiTapeStep:
    """İki şerit anlık görünümü."""

    state: str
    tape0: str
    tape1: str
    head0: int
    head1: int


@dataclass
class MultiTapeRunResult:
    accepted: bool
    reason: str
    final_tape0: str
    final_tape1: str
    steps: int
    history: List[MultiTapeStep] = field(default_factory=list)


class MultiTapeTM:
    """İki şeritli deterministik TM (bonus)."""

    def __init__(
        self,
        name: str,
        states: List[str],
        input_alphabet: List[str],
        tape_alphabet: List[str],
        blank: str,
        start_state: str,
        accept_states: List[str],
        reject_states: List[str],
        transitions: Mapping[Tuple[str, str, str], Tuple[str, str, str, Move, Move]],
        description: str = "",
    ) -> None:
        self.name = name
        self.description = description
        self.states = states
        self.input_alphabet = input_alphabet
        self.tape_alphabet = tape_alphabet
        self.blank = blank
        self.start_state = start_state
        self.accept_states = set(accept_states)
        self.reject_states = set(reject_states)
        self._transitions = dict(transitions)

    @classmethod
    def from_yaml(cls, path: str | Path) -> MultiTapeTM:
        p = Path(path)
        if not p.is_file():
            raise ValueError(f"YAML dosyası bulunamadı: {p}")
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Kök YAML bir nesne olmalıdır.")
        return cls._from_mapping(data, source=str(p))

    @classmethod
    def _from_mapping(cls, data: dict[str, Any], source: str = "") -> MultiTapeTM:
        prefix = f"{source}: " if source else ""
        for key in (
            "name",
            "states",
            "input_alphabet",
            "tape_alphabet",
            "blank",
            "start_state",
            "accept_states",
            "transitions",
        ):
            if key not in data:
                raise ValueError(f"{prefix}Eksik alan: {key!r}")

        blank = str(data["blank"])
        if len(blank) != 1:
            raise ValueError(f"{prefix}blank tek karakter olmalıdır.")

        transitions: dict[Tuple[str, str, str], Tuple[str, str, str, Move, Move]] = {}
        raw = data["transitions"]
        if not isinstance(raw, list):
            raise ValueError(f"{prefix}transitions bir liste olmalıdır.")

        for i, row in enumerate(raw):
            if not isinstance(row, dict):
                raise ValueError(f"{prefix}transitions[{i}] nesne olmalıdır.")
            st = str(row["state"])
            reads = row.get("read")
            if not isinstance(reads, list) or len(reads) != 2:
                raise ValueError(f"{prefix}transitions[{i}] read iki elemanlı liste olmalıdır.")
            r0, r1 = str(reads[0]), str(reads[1])
            writes = row.get("write")
            if not isinstance(writes, list) or len(writes) != 2:
                raise ValueError(f"{prefix}transitions[{i}] write iki elemanlı liste olmalıdır.")
            w0, w1 = str(writes[0]), str(writes[1])
            moves = row.get("move")
            if not isinstance(moves, list) or len(moves) != 2:
                raise ValueError(f"{prefix}transitions[{i}] move iki elemanlı liste olmalıdır.")
            m0, m1 = str(moves[0]), str(moves[1])
            if m0 not in ("L", "R") or m1 not in ("L", "R"):
                raise ValueError(f"{prefix}transitions[{i}] move yalnızca L veya R olabilir.")
            nxt = str(row["next"])
            key = (st, r0, r1)
            if key in transitions:
                raise ValueError(f"{prefix}Yinelenen geçiş: state={st!r} read={reads!r}")
            transitions[key] = (nxt, w0, w1, m0, m1)

        return cls(
            name=str(data["name"]),
            states=_as_str_list(data["states"], "states", prefix),
            input_alphabet=_as_str_list(data["input_alphabet"], "input_alphabet", prefix),
            tape_alphabet=_as_str_list(data["tape_alphabet"], "tape_alphabet", prefix),
            blank=blank,
            start_state=str(data["start_state"]),
            accept_states=_as_str_list(data["accept_states"], "accept_states", prefix),
            reject_states=_as_str_list(data.get("reject_states", []), "reject_states", prefix),
            transitions=transitions,
            description=str(data.get("description", "")),
        )

    def run(
        self,
        input_string: str,
        *,
        max_steps: int = 10_000,
        verbose: bool = False,
    ) -> MultiTapeRunResult:
        for ch in input_string:
            if ch not in self.input_alphabet:
                raise ValueError(f"Girdi sembolü input_alphabet dışında: {ch!r}")

        t0: dict[int, str] = {i: input_string[i] for i in range(len(input_string))}
        t1: dict[int, str] = {}
        h0, h1 = 0, 0
        state = self.start_state
        history: list[MultiTapeStep] = []

        def read(tape: dict[int, str], head: int) -> str:
            return tape.get(head, self.blank)

        def span(tape: dict[int, str], head: int) -> tuple[int, int]:
            keys = list(tape.keys())
            lo = min(keys + [head]) if keys else head
            hi = max(keys + [head]) if keys else head
            return min(lo, head), max(hi, head)

        def show(tape: dict[int, str], head: int) -> str:
            lo, hi = span(tape, head)
            return "".join(tape.get(i, self.blank) for i in range(lo, hi + 1))

        def rel(tape: dict[int, str], head: int) -> int:
            lo, _ = span(tape, head)
            return head - lo

        history.append(
            MultiTapeStep(
                state=state,
                tape0=show(t0, h0),
                tape1=show(t1, h1),
                head0=rel(t0, h0),
                head1=rel(t1, h1),
            )
        )

        steps = 0
        while steps < max_steps:
            if state in self.accept_states:
                return MultiTapeRunResult(
                    accepted=True,
                    reason="accept",
                    final_tape0=_strip_blanks(show(t0, h0), self.blank),
                    final_tape1=_strip_blanks(show(t1, h1), self.blank),
                    steps=steps,
                    history=history,
                )
            if state in self.reject_states:
                return MultiTapeRunResult(
                    accepted=False,
                    reason="reject",
                    final_tape0=_strip_blanks(show(t0, h0), self.blank),
                    final_tape1=_strip_blanks(show(t1, h1), self.blank),
                    steps=steps,
                    history=history,
                )

            key = (state, read(t0, h0), read(t1, h1))
            if key not in self._transitions:
                return MultiTapeRunResult(
                    accepted=False,
                    reason="no_transition",
                    final_tape0=_strip_blanks(show(t0, h0), self.blank),
                    final_tape1=_strip_blanks(show(t1, h1), self.blank),
                    steps=steps,
                    history=history,
                )

            nxt, w0, w1, m0, m1 = self._transitions[key]
            if verbose:
                print(
                    f"Adım {steps} | {state} | T0: {show(t0, h0)} | T1: {show(t1, h1)}"
                )

            if w0 != self.blank or h0 in t0:
                if w0 == self.blank:
                    t0.pop(h0, None)
                else:
                    t0[h0] = w0
            if w1 != self.blank or h1 in t1:
                if w1 == self.blank:
                    t1.pop(h1, None)
                else:
                    t1[h1] = w1

            state = nxt
            h0 += 1 if m0 == "R" else -1
            h1 += 1 if m1 == "R" else -1
            steps += 1

            history.append(
                MultiTapeStep(
                    state=state,
                    tape0=show(t0, h0),
                    tape1=show(t1, h1),
                    head0=rel(t0, h0),
                    head1=rel(t1, h1),
                )
            )

            if state in self.accept_states:
                return MultiTapeRunResult(
                    accepted=True,
                    reason="accept",
                    final_tape0=_strip_blanks(show(t0, h0), self.blank),
                    final_tape1=_strip_blanks(show(t1, h1), self.blank),
                    steps=steps,
                    history=history,
                )
            if state in self.reject_states:
                return MultiTapeRunResult(
                    accepted=False,
                    reason="reject",
                    final_tape0=_strip_blanks(show(t0, h0), self.blank),
                    final_tape1=_strip_blanks(show(t1, h1), self.blank),
                    steps=steps,
                    history=history,
                )

        return MultiTapeRunResult(
            accepted=False,
            reason="timeout",
            final_tape0=_strip_blanks(show(t0, h0), self.blank),
            final_tape1=_strip_blanks(show(t1, h1), self.blank),
            steps=steps,
            history=history,
        )
