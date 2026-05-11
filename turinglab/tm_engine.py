"""Tek şeritli deterministik Turing makinesi motoru."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple

import yaml

Move = str  # "L" | "R"


@dataclass(frozen=True)
class TMStep:
    """Tek adımdaki anlık yapılandırma (history öğesi)."""

    state: str
    tape: str
    head_position: int


@dataclass
class RunResult:
    """Çalıştırma sonucu."""

    accepted: bool
    reason: str
    final_tape: str
    steps: int
    history: List[TMStep] = field(default_factory=list)


class SingleTapeTM:
    """YAML dosyasından yüklenen tek şeritli deterministik TM."""

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
        transitions: Mapping[Tuple[str, str], Tuple[str, str, Move]],
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
    def from_yaml(cls, path: str | Path) -> SingleTapeTM:
        p = Path(path)
        if not p.is_file():
            raise ValueError(f"YAML dosyası bulunamadı: {p}")
        raw = p.read_text(encoding="utf-8")
        try:
            data = yaml.safe_load(raw)
        except yaml.YAMLError as e:
            raise ValueError(f"YAML ayrıştırma hatası: {e}") from e
        if not isinstance(data, dict):
            raise ValueError("Kök YAML bir nesne (mapping) olmalıdır.")
        return cls._from_mapping(data, source=str(p))

    @classmethod
    def _from_mapping(cls, data: dict[str, Any], source: str = "") -> SingleTapeTM:
        prefix = f"{source}: " if source else ""
        required = [
            "name",
            "states",
            "input_alphabet",
            "tape_alphabet",
            "blank",
            "start_state",
            "accept_states",
            "transitions",
        ]
        for key in required:
            if key not in data:
                raise ValueError(f"{prefix}Eksik alan: {key!r}")

        name = str(data["name"])
        states = _as_str_list(data["states"], "states", prefix)
        input_alphabet = _as_str_list(data["input_alphabet"], "input_alphabet", prefix)
        tape_alphabet = _as_str_list(data["tape_alphabet"], "tape_alphabet", prefix)
        blank = str(data["blank"])
        if len(blank) != 1:
            raise ValueError(f"{prefix}blank tek karakter olmalıdır, alındı: {blank!r}")
        start_state = str(data["start_state"])
        accept_states = _as_str_list(data["accept_states"], "accept_states", prefix)
        reject_states = _as_str_list(data.get("reject_states", []), "reject_states", prefix)
        transitions_raw = data["transitions"]
        if not isinstance(transitions_raw, list):
            raise ValueError(f"{prefix}transitions bir liste olmalıdır.")

        state_set = set(states)
        if blank not in tape_alphabet:
            raise ValueError(f"{prefix}blank sembolü tape_alphabet içinde olmalıdır.")
        for s in input_alphabet:
            if s not in tape_alphabet:
                raise ValueError(
                    f"{prefix}input_alphabet sembolü tape_alphabet içinde değil: {s!r}"
                )
        if start_state not in state_set:
            raise ValueError(f"{prefix}start_state tanımlı durumlarda değil: {start_state!r}")
        for s in accept_states:
            if s not in state_set:
                raise ValueError(f"{prefix}accept_states içinde bilinmeyen durum: {s!r}")
        for s in reject_states:
            if s not in state_set:
                raise ValueError(f"{prefix}reject_states içinde bilinmeyen durum: {s!r}")

        transitions: dict[Tuple[str, str], Tuple[str, str, Move]] = {}
        seen: set[Tuple[str, str]] = set()
        for i, row in enumerate(transitions_raw):
            if not isinstance(row, dict):
                raise ValueError(f"{prefix}transitions[{i}] bir nesne olmalıdır.")
            for f in ("state", "read", "next", "write", "move"):
                if f not in row:
                    raise ValueError(f"{prefix}transitions[{i}] eksik alan: {f!r}")
            st, rd, nx, wr, mv = (
                str(row["state"]),
                str(row["read"]),
                str(row["next"]),
                str(row["write"]),
                str(row["move"]).upper(),
            )
            if mv not in ("L", "R"):
                raise ValueError(f"{prefix}transitions[{i}] move L veya R olmalı, alındı: {mv!r}")
            if len(wr) != 1:
                raise ValueError(f"{prefix}transitions[{i}] write tek karakter olmalıdır.")
            if len(rd) != 1:
                raise ValueError(f"{prefix}transitions[{i}] read tek karakter olmalıdır.")
            if st not in state_set or nx not in state_set:
                raise ValueError(f"{prefix}transitions[{i}] bilinmeyen durum.")
            if rd not in tape_alphabet or wr not in tape_alphabet:
                raise ValueError(
                    f"{prefix}transitions[{i}] read/write tape_alphabet dışında: {rd!r}/{wr!r}"
                )
            key = (st, rd)
            if key in seen:
                raise ValueError(
                    f"{prefix}Yinelenen geçiş (deterministik TM): state={st!r} read={rd!r}"
                )
            seen.add(key)
            transitions[key] = (nx, wr, mv)

        description = str(data.get("description", ""))
        return cls(
            name=name,
            states=states,
            input_alphabet=input_alphabet,
            tape_alphabet=tape_alphabet,
            blank=blank,
            start_state=start_state,
            accept_states=accept_states,
            reject_states=reject_states,
            transitions=transitions,
            description=description,
        )

    def run(
        self,
        input_string: str = "",
        max_steps: int = 10_000,
        verbose: bool = False,
    ) -> RunResult:
        for ch in input_string:
            if ch not in self.input_alphabet:
                raise ValueError(
                    f"Girdi sembolü input_alphabet dışında: {ch!r} (izin verilen: {self.input_alphabet})"
                )

        tape: dict[int, str] = {i: input_string[i] for i in range(len(input_string))}
        head = 0
        state = self.start_state
        history: list[TMStep] = []

        def read_cell() -> str:
            return tape.get(head, self.blank)

        def write_cell(sym: str) -> None:
            if sym == self.blank and head not in tape:
                return
            if sym == self.blank:
                tape.pop(head, None)
            else:
                tape[head] = sym

        def span() -> tuple[int, int]:
            keys = list(tape.keys())
            lo = min(keys + [head]) if keys else head
            hi = max(keys + [head]) if keys else head
            lo = min(lo, head)
            hi = max(hi, head)
            return lo, hi

        def tape_string() -> str:
            lo, hi = span()
            return "".join(tape.get(i, self.blank) for i in range(lo, hi + 1))

        def head_index_in_display() -> int:
            lo, _ = span()
            return head - lo

        history.append(TMStep(state=state, tape=tape_string(), head_position=head_index_in_display()))

        steps = 0
        while steps < max_steps:
            if state in self.accept_states:
                return RunResult(
                    accepted=True,
                    reason="accept",
                    final_tape=_strip_blanks(tape_string(), self.blank),
                    steps=steps,
                    history=history,
                )
            if state in self.reject_states:
                return RunResult(
                    accepted=False,
                    reason="reject",
                    final_tape=_strip_blanks(tape_string(), self.blank),
                    steps=steps,
                    history=history,
                )

            sym = read_cell()
            key = (state, sym)
            if key not in self._transitions:
                return RunResult(
                    accepted=False,
                    reason="no_transition",
                    final_tape=_strip_blanks(tape_string(), self.blank),
                    steps=steps,
                    history=history,
                )

            nxt, wrt, move = self._transitions[key]
            if verbose:
                lo, hi = span()
                disp = _format_tape_verbose(lo, hi, tape, head, self.blank)
                print(f"Adım {steps} | Durum: {state} | Şerit: {disp} | Hareket: {move}")

            write_cell(wrt)
            state = nxt
            if move == "R":
                head += 1
            else:
                head -= 1
            steps += 1

            lo, hi = span()
            rel = head - lo
            history.append(TMStep(state=state, tape=tape_string(), head_position=rel))

            if state in self.accept_states:
                return RunResult(
                    accepted=True,
                    reason="accept",
                    final_tape=_strip_blanks(tape_string(), self.blank),
                    steps=steps,
                    history=history,
                )
            if state in self.reject_states:
                return RunResult(
                    accepted=False,
                    reason="reject",
                    final_tape=_strip_blanks(tape_string(), self.blank),
                    steps=steps,
                    history=history,
                )

        return RunResult(
            accepted=False,
            reason="timeout",
            final_tape=_strip_blanks(tape_string(), self.blank),
            steps=steps,
            history=history,
        )


def _as_str_list(value: Any, field: str, prefix: str) -> List[str]:
    if not isinstance(value, list):
        raise ValueError(f"{prefix}{field} bir liste olmalıdır.")
    out: list[str] = []
    for i, x in enumerate(value):
        if isinstance(x, str):
            out.append(x)
        elif x is None:
            raise ValueError(f"{prefix}{field}[{i}] geçersiz.")
        else:
            out.append(str(x))
    return out


def _strip_blanks(s: str, blank: str) -> str:
    if not s:
        return s
    chars = list(s)
    while chars and chars[0] == blank:
        chars.pop(0)
    while chars and chars[-1] == blank:
        chars.pop()
    return "".join(chars)


def _format_tape_verbose(
    lo: int,
    hi: int,
    tape: dict[int, str],
    head: int,
    blank: str,
) -> str:
    parts: list[str] = []
    for i in range(lo, hi + 1):
        ch = tape.get(i, blank)
        if i == head:
            parts.append(f"[{ch}]")
        else:
            parts.append(ch)
    return "".join(parts)
