"""Şerit görselleştirme — PPM ve isteğe bağlı GIF (bonus)."""

from __future__ import annotations

from pathlib import Path
from typing import List, Sequence, Union

from turinglab import RunResult, TMStep
from turinglab.bonus.multi_tape import MultiTapeStep

TapeHistory = Union[RunResult, Sequence[TMStep], Sequence[MultiTapeStep]]


def _cell_color(ch: str, is_head: bool) -> tuple[int, int, int]:
    if is_head:
        return (220, 80, 60)
    if ch in ("0", "1"):
        return (70, 130, 200)
    if ch in ("a", "b"):
        return (90, 170, 90)
    if ch == "#":
        return (160, 120, 200)
    return (240, 240, 235)


def write_ppm_frame(
    path: str | Path,
    tape: str,
    head: int,
    *,
    cell: int = 20,
    label: str = "",
) -> None:
    """ASCII PPM (P3) — Pillow ile uyumlu."""
    path = Path(path)
    n = max(len(tape), 1)
    label_h = 18 if label else 0
    width = n * cell
    height = label_h + cell

    lines = ["P3", f"{width} {height}", "255"]
    if label:
        for _ in range(label_h):
            for _ in range(width):
                lines.append("40 40 40")
    for _ in range(cell):
        for i in range(n):
            ch = tape[i] if i < len(tape) else "B"
            rgb = _cell_color(ch, i == head)
            for _ in range(cell):
                lines.append(f"{rgb[0]} {rgb[1]} {rgb[2]}")
    path.write_text("\n".join(lines) + "\n", encoding="ascii")


def _iter_steps(history_or_result: TapeHistory) -> List[tuple[str, int, str]]:
    if isinstance(history_or_result, RunResult):
        steps = history_or_result.history
    else:
        steps = list(history_or_result)
    out: list[tuple[str, int, str]] = []
    for step in steps:
        if isinstance(step, MultiTapeStep):
            out.append((f"{step.tape0}|{step.tape1}", step.head0, step.state))
        else:
            out.append((step.tape, step.head_position, step.state))
    return out


def export_history_ppm(
    history_or_result: TapeHistory,
    out_dir: str | Path,
    *,
    prefix: str = "frame",
) -> List[Path]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for i, (tape, head, state) in enumerate(_iter_steps(history_or_result)):
        p = out / f"{prefix}_{i:04d}.ppm"
        write_ppm_frame(p, tape, head, label=state)
        paths.append(p)
    return paths


def export_history_gif(
    history_or_result: TapeHistory,
    out_path: str | Path,
    *,
    duration_ms: int = 200,
    cell: int = 16,
) -> bool:
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return False

    out_path = Path(out_path)
    frames: list[Image.Image] = []
    for tape, head, state in _iter_steps(history_or_result):
        n = max(len(tape), 1)
        w, h = n * cell + 40, cell + 30
        img = Image.new("RGB", (w, h), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text((4, 2), state, fill=(30, 30, 30))
        y0 = 22
        for i, ch in enumerate(tape):
            x0 = 20 + i * cell
            rgb = _cell_color(ch, i == head)
            draw.rectangle([x0, y0, x0 + cell - 2, y0 + cell - 2], fill=rgb)
        frames.append(img)

    if not frames:
        return False

    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms,
        loop=0,
    )
    return True
