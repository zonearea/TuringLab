#!/usr/bin/env python3
"""TuringLab video sunumu için terminal demoları (Bölüm 1–8).

Kullanım:
  python scripts/demo_video.py --all
  python scripts/demo_video.py --section 3
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from turinglab import SingleTapeTM  # noqa: E402


def _utf8_stdout() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:
                pass


def _banner(title: str) -> None:
    line = "=" * 60
    print(f"\n{line}\n  {title}\n{line}\n")


def _run_tm(
    yaml_name: str,
    inp: str,
    *,
    verbose: bool = True,
    max_steps: int = 500_000,
) -> None:
    path = ROOT / "machines" / yaml_name
    tm = SingleTapeTM.from_yaml(path)
    print(f"Makine: {yaml_name}")
    print(f"Girdi:  {inp!r}\n")
    r = tm.run(input_string=inp, max_steps=max_steps, verbose=verbose)
    print(
        f"\nSonuç: {r.reason} | şerit: {r.final_tape.strip('B')!r} | adım: {r.steps}"
    )


def section_1() -> None:
    _banner("Bölüm 1 — Giriş")
    print("Proje: TuringLab — tek şeritli deterministik TM (YAML + pytest)")
    print(f"Kök dizin: {ROOT}")
    print("Dosyalar: README.md, REPORT.md, machines/, turinglab/")


def section_2() -> None:
    _banner("Bölüm 2 — Motor: seyrek şerit (dict)")
    engine = ROOT / "turinglab" / "tm_engine.py"
    print(f"Dosya: {engine.relative_to(ROOT)}")
    print("\nÖnemli satırlar (tape sözlüğü):")
    text = engine.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(text, start=1):
        if "tape: dict[int, str]" in line or "tape.get(head" in line or "head -= 1" in line:
            print(f"  {i:4d} | {line.rstrip()}")


def section_3() -> None:
    _banner("Bölüm 3 — TM-1 unary_to_binary (girdi 111 → ikili 11)")
    _run_tm("unary_to_binary.yaml", "111")


def section_4() -> None:
    _banner("Bölüm 4 — TM-2 binary_compare (1100#1011 → kabul)")
    _run_tm("binary_compare.yaml", "1100#1011")


def section_5() -> None:
    _banner("Bölüm 5 — TM-3 string_copy (ab → ab#ab)")
    print(
        "Not (yaşanan sorunlar):\n"
        "  1) # yazıldıktan sonra kafa sağa gidince q_loop boşlukta ret.\n"
        "  2) X işareti kopyadan önce silinince yarım kopya (ab#a).\n"
        "Düzeltme: q_run→#+L, q_mka/q_mkb + q_reta/q_retb.\n"
    )
    _run_tm("string_copy.yaml", "ab")


def section_6() -> None:
    _banner("Bölüm 6 — TM-4 unary_div3")
    path = ROOT / "machines" / "unary_div3.yaml"
    tm = SingleTapeTM.from_yaml(path)
    cases = [
        ("111", "3 → kabul"),
        ("111111", "6 → kabul"),
        ("11", "2 → ret"),
    ]
    for inp, label in cases:
        r = tm.run(input_string=inp, max_steps=50_000, verbose=False)
        print(f"  {inp!r:8s} → {r.reason:6s}  ({label})")


def section_7() -> None:
    _banner("Bölüm 7 — pytest tests/ -v")
    print("Komut: python -m pytest tests/ -v\n")
    subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=no"],
        cwd=ROOT,
        check=False,
    )


def section_8() -> None:
    _banner("Bölüm 8 — Kapanış")
    print(
        "Öğrenilenler:\n"
        "  • Deterministik TM: (durum, okunan) → tek geçiş\n"
        "  • TM-2: sağ şerit de işaretlenmeli\n"
        "  • TM-3: X işareti kopya bitene kadar korunmalı\n"
        "  • pytest regresyon testleri\n"
        "\nTeşekkürler."
    )


SECTIONS = {
    1: section_1,
    2: section_2,
    3: section_3,
    4: section_4,
    5: section_5,
    6: section_6,
    7: section_7,
    8: section_8,
}


def main() -> None:
    _utf8_stdout()
    p = argparse.ArgumentParser(description="TuringLab video sunum demoları")
    p.add_argument("--section", type=int, choices=list(SECTIONS), help="Tek bölüm (1–8)")
    p.add_argument("--all", action="store_true", help="Tüm bölümleri sırayla çalıştır")
    args = p.parse_args()

    if args.all:
        for n in sorted(SECTIONS):
            SECTIONS[n]()
        return

    if args.section is None:
        p.print_help()
        print("\nÖrnek: python scripts/demo_video.py --section 3")
        sys.exit(0)

    SECTIONS[args.section]()


if __name__ == "__main__":
    main()
