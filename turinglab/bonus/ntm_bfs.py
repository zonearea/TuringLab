"""Belirsiz TM — BFS ile simülasyon (bonus)."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Mapping, Sequence, Tuple

Move = str
FrozenTape = Tuple[Tuple[int, str], ...]
ConfigSig = Tuple[FrozenTape, int, str]


@dataclass(frozen=True)
class NTMStep:
    state: str
    tape: str
    head_position: int


@dataclass
class BFSResult:
    """BFS sonucu: ilk kabul yolu veya tüm yolların özeti."""

    found: bool
    reason: str
    steps: int
    paths_explored: int
    history: List[NTMStep] = field(default_factory=list)


class NondeterministicTM:
    """Tek şeritli NTM; her (durum, okunan) için birden fazla geçiş."""

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
        transitions: Mapping[Tuple[str, str], Sequence[Tuple[str, str, Move]]],
    ) -> None:
        self.name = name
        self.states = states
        self.input_alphabet = input_alphabet
        self.tape_alphabet = tape_alphabet
        self.blank = blank
        self.start_state = start_state
        self.accept_states = set(accept_states)
        self.reject_states = set(reject_states)
        self._transitions = {k: list(v) for k, v in transitions.items()}

    def run_bfs(
        self,
        input_string: str,
        *,
        max_steps: int = 50,
        max_nodes: int = 5000,
    ) -> BFSResult:
        for ch in input_string:
            if ch not in self.input_alphabet:
                raise ValueError(f"Girdi sembolü input_alphabet dışında: {ch!r}")

        start_tape: Dict[int, str] = {i: input_string[i] for i in range(len(input_string))}
        start_head = 0
        start_state = self.start_state

        def read_cell(tape: Dict[int, str], head: int) -> str:
            return tape.get(head, self.blank)

        def tape_str(tape: Dict[int, str], head: int) -> tuple[str, int]:
            keys = list(tape.keys())
            lo = min(keys + [head]) if keys else head
            hi = max(keys + [head]) if keys else head
            lo = min(lo, head)
            hi = max(hi, head)
            s = "".join(tape.get(i, self.blank) for i in range(lo, hi + 1))
            return s, head - lo

        def apply(
            tape: Dict[int, str],
            head: int,
            state: str,
            nxt: str,
            wrt: str,
            move: Move,
        ) -> tuple[Dict[int, str], int, str]:
            new_tape = dict(tape)
            if wrt == self.blank:
                new_tape.pop(head, None)
            else:
                new_tape[head] = wrt
            new_head = head + (1 if move == "R" else -1)
            return new_tape, new_head, nxt

        # (tape_frozen, head, state, steps, history)
        def freeze(tape: Dict[int, str]) -> tuple[tuple[int, str], ...]:
            return tuple(sorted(tape.items()))

        start_frozen = freeze(start_tape)
        queue: deque[
            tuple[
                tuple[tuple[int, str], ...],
                int,
                str,
                int,
                List[NTMStep],
            ]
        ] = deque()
        queue.append((start_frozen, start_head, start_state, 0, []))
        visited: set[ConfigSig] = set()
        visited.add((start_frozen, start_head, start_state))
        paths = 0

        while queue and paths < max_nodes:
            frozen, head, state, steps, hist = queue.popleft()
            tape = dict(frozen)
            paths += 1

            if state in self.accept_states:
                ts, rel = tape_str(tape, head)
                return BFSResult(
                    found=True,
                    reason="accept",
                    steps=steps,
                    paths_explored=paths,
                    history=hist + [NTMStep(state=state, tape=ts, head_position=rel)],
                )
            if state in self.reject_states:
                continue
            if steps >= max_steps:
                continue

            sym = read_cell(tape, head)
            key = (state, sym)
            if key not in self._transitions:
                continue

            ts, rel = tape_str(tape, head)
            base_hist = hist + [NTMStep(state=state, tape=ts, head_position=rel)]

            for nxt, wrt, move in self._transitions[key]:
                new_tape, new_head, new_state = apply(tape, head, state, nxt, wrt, move)
                new_frozen = freeze(new_tape)
                sig = (new_frozen, new_head, new_state)
                if sig in visited:
                    continue
                visited.add(sig)
                queue.append((new_frozen, new_head, new_state, steps + 1, base_hist))

        return BFSResult(
            found=False,
            reason="no_accept_path",
            steps=0,
            paths_explored=paths,
            history=[],
        )
