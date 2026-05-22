#!/usr/bin/env python3
"""TuringLab — makineleri adım adım terminal çıktısı.

Tek makine:
  python demo.py binary_increment
  python demo.py unary_to_binary
  python demo.py tm2

Tümü:
  python demo.py
  python demo.py --only odev

Liste: python demo.py --list
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from turinglab import SingleTapeTM  # noqa: E402


@dataclass(frozen=True)
class DemoCase:
    id: str
    yaml: str
    girdi: str
    aciklama: str
    grup: str
    girdi_kurali: str
    kabul_kurali: str
    ornek_cikti: str


ORNEKLER: list[DemoCase] = [
    DemoCase(
        "binary_increment",
        "binary_increment.yaml",
        "1011",
        "İkili sayı +1 (el kitabı)",
        "ornek",
        "Girdi: {0,1}+",
        "Kabul: şerit girdi+1 ikili sayı",
        "1011 → 1100",
    ),
    DemoCase(
        "unary_increment",
        "unary_increment.yaml",
        "111",
        "Unary 1^n → bir 1 ekle",
        "ornek",
        "Girdi: 1+",
        "Kabul: şerit bir 1 uzamış unary",
        "111 → 1111",
    ),
    DemoCase(
        "even_a",
        "even_a.yaml",
        "abab",
        "Çift sayıda 'a' harfi",
        "ornek",
        "Girdi: {a,b}*",
        "Kabul: 'a' sayısı çift",
        "abab → kabul, ab → ret",
    ),
    DemoCase(
        "binary_palindrome",
        "binary_palindrome.yaml",
        "0110",
        "0/1 palindrom",
        "ornek",
        "Girdi: {0,1}*",
        "Kabul: şerit palindrom",
        "0110 → kabul",
    ),
]

ODEV: list[DemoCase] = [
    DemoCase(
        "unary_to_binary",
        "unary_to_binary.yaml",
        "111",
        "TM-1: unary → ikili (3 → 11)",
        "odev",
        "Girdi: 1^n, n≥1; n≤255",
        "Kabul: şerit = n’nin ikili yazımı (baştaki 0’lar silinir)",
        "111 → şerit 11",
    ),
    DemoCase(
        "binary_compare",
        "binary_compare.yaml",
        "1100#1011",
        "TM-2: sol ikili > sağ (12 > 11)",
        "odev",
        "Girdi: w#v, w,v ∈ {0,1}*",
        "Kabul: sol ikili sayı > sağ ikili sayı (MSB önce)",
        "1100#1011 → kabul; 11#11 → ret",
    ),
    DemoCase(
        "string_copy",
        "string_copy.yaml",
        "abba",
        "TM-3: w → w#w",
        "odev",
        "Girdi: {a,b}+",
        "Kabul: şerit w#w biçiminde tam kopya",
        "abba → abba#abba",
    ),
    DemoCase(
        "unary_div3",
        "unary_div3.yaml",
        "111",
        "TM-4: 1^n, n mod 3 = 0",
        "odev",
        "Girdi: 1+ veya boş (boş ret)",
        "Kabul: n, 3’ün katı",
        "111 → kabul; 11 → ret",
    ),
]

TUMU = ORNEKLER + ODEV

# Kısa takma adlar (video / kolay yazım)
ALIASES: dict[str, str] = {
    "tm1": "unary_to_binary",
    "tm2": "binary_compare",
    "tm3": "string_copy",
    "tm4": "unary_div3",
    "increment": "binary_increment",
    "palindrome": "binary_palindrome",
}

BY_ID: dict[str, DemoCase] = {c.id: c for c in TUMU}


def _utf8_stdout() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:
                pass


def _ayirici(baslik: str) -> None:
    print("\n" + "=" * 72)
    print(f"  {baslik}")
    print("=" * 72 + "\n")


def _resolve_id(name: str) -> str:
    key = name.lower().removesuffix(".yaml")
    if key in ALIASES:
        return ALIASES[key]
    return key


def _calistir(case: DemoCase, *, girdi: str | None, verbose: bool, max_steps: int) -> None:
    inp = girdi if girdi is not None else case.girdi
    path = ROOT / "machines" / case.yaml
    tm = SingleTapeTM.from_yaml(path)
    print(f"Komut : python demo.py {case.id}")
    print(f"Dosya : machines/{case.yaml}")
    print(f"Görev : {case.aciklama}")
    print(f"Girdi kuralı  : {case.girdi_kurali}")
    print(f"Kabul kuralı  : {case.kabul_kurali}")
    print(f"Örnek         : {case.ornek_cikti}")
    print(f"Bu çalıştırma : girdi={inp!r}\n")
    if verbose:
        print("--- Adımlar (Adım | Durum | Şerit | Hareket) ---\n")
    r = tm.run(input_string=inp, max_steps=max_steps, verbose=verbose)
    tape = r.final_tape.strip("B")
    print(f"\n>>> Sonuç: {r.reason} | şerit: {tape!r} | toplam adım: {r.steps}\n")


def main() -> None:
    _utf8_stdout()
    p = argparse.ArgumentParser(
        description="TuringLab — tek makine veya sırayla tümü.",
        epilog="Örnek: python demo.py binary_compare",
    )
    p.add_argument(
        "makine",
        nargs="?",
        help="Makine adı (binary_increment, unary_to_binary, tm2, …)",
    )
    p.add_argument(
        "--only",
        choices=("ornek", "odev", "all"),
        default="all",
        help="makine verilmezse hangi grup çalışsın",
    )
    p.add_argument("--girdi", help="Varsayılan girdi yerine özel girdi")
    p.add_argument("--quiet", action="store_true", help="Yalnızca sonuç satırı")
    p.add_argument("--list", action="store_true", help="Komut listesi")
    p.add_argument("--max-steps", type=int, default=500_000)
    args = p.parse_args()

    if args.list:
        print("Her makine için komut:\n")
        for c in TUMU:
            print(f"  python demo.py {c.id:<22}  # {c.aciklama}")
        print("\nTakma adlar: tm1 tm2 tm3 tm4  |  Gruplar: python demo.py --only odev")
        return

    verbose = not args.quiet

    if args.makine:
        mid = _resolve_id(args.makine)
        if mid not in BY_ID:
            print(f"Bilinmeyen makine: {args.makine!r}", file=sys.stderr)
            print("python demo.py --list", file=sys.stderr)
            sys.exit(1)
        case = BY_ID[mid]
        print("TuringLab demo\n")
        _ayirici(case.yaml)
        _calistir(case, girdi=args.girdi, verbose=verbose, max_steps=args.max_steps)
        return

    if args.only == "ornek":
        cases, baslik = ORNEKLER, "Bölüm 1 — Örnek makineler"
    elif args.only == "odev":
        cases, baslik = ODEV, "Bölüm 2 — Ödev makineleri"
    else:
        cases, baslik = TUMU, "Tüm makineler (sırayla)"

    print("TuringLab demo\n")
    _ayirici(baslik)
    for i, case in enumerate(cases, start=1):
        if len(cases) > 1:
            _ayirici(f"[{i}/{len(cases)}] python demo.py {case.id}")
        _calistir(case, girdi=None, verbose=verbose, max_steps=args.max_steps)

    if len(cases) > 1:
        print("=" * 72)
        print("  Bitti. Tek makine: python demo.py <ad>")
        print("=" * 72)


if __name__ == "__main__":
    main()
