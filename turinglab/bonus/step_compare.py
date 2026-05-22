"""Adım sayısı karşılaştırma ve grafik (bonus)."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from turinglab import SingleTapeTM


@dataclass
class StepComparison:
    """Etiket → adım sayısı tablosu."""

    labels: List[str]
    steps: List[int]
    reasons: List[str]

    def as_dict(self) -> Dict[str, int]:
        return dict(zip(self.labels, self.steps))


def compare_step_counts(
    tm: SingleTapeTM,
    cases: Sequence[Tuple[str, str]],
    *,
    max_steps: int = 100_000,
) -> StepComparison:
    """Her (etiket, girdi) için ``run`` adım sayısını toplar."""
    labels: list[str] = []
    steps: list[int] = []
    reasons: list[str] = []
    for label, inp in cases:
        r = tm.run(inp, max_steps=max_steps, verbose=False)
        labels.append(label)
        steps.append(r.steps)
        reasons.append(r.reason)
    return StepComparison(labels=labels, steps=steps, reasons=reasons)


def save_comparison(
    comparison: StepComparison,
    out_dir: str | Path,
    *,
    basename: str = "steps",
) -> Dict[str, Path]:
    """CSV ve isteğe bağlı PNG grafik yazar."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    csv_path = out / f"{basename}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["label", "steps", "reason"])
        for lab, st, rea in zip(comparison.labels, comparison.steps, comparison.reasons):
            w.writerow([lab, st, rea])

    written: dict[str, Path] = {"csv": csv_path}
    png_path = out / f"{basename}.png"
    if _save_png(comparison, png_path):
        written["png"] = png_path
    return written


def _save_png(comparison: StepComparison, path: Path) -> bool:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return False

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(comparison.labels, comparison.steps, color="#4a90d9")
    ax.set_ylabel("Adım sayısı")
    ax.set_title("TM adım karşılaştırması")
    plt.xticks(rotation=25, ha="right")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return True
