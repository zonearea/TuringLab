# TuringLab — Mini-rapor (Bölüm 3)

**Öğrenci:** Hüseyin Berkay Kayıkçı  
**Proje:** `turinglab` — tek şeritli deterministik TM motoru (YAML + pytest)

## Özet

Python paketi `turinglab` ile YAML tanımlı Turing makineleri yüklenip simüle edilir. Bölüm 1’de motor ve el kitabı örnekleri; Bölüm 2’de dört ödev makinesi (unary→binary, ikili karşılaştırma, dize kopyalama, unary mod 3) tamamlandı. Testler: `python -m pytest tests/ -q`.

## Bölüm 1 — Motor

- `SingleTapeTM.from_yaml`, `run`: kabul, ret, `no_transition`, `timeout`.
- Seyrek şerit, negatif kafa indeksi.
- Örnekler: `binary_increment`, `unary_increment`, `even_a`, `binary_palindrome`.
- Testler: `tests/test_tm_engine.py`.

## Bölüm 2 — Ödev makineleri

| TM | Dosya | Görev |
|----|-------|--------|
| TM-1 | `unary_to_binary.yaml` | `1^n` → n’nin ikili yazımı (n≤255) |
| TM-2 | `binary_compare.yaml` | Sol ikili > sağ ikili ise kabul (`1100#1011`) |
| TM-3 | `string_copy.yaml` | `w` → `w#w` (`abba` → `abba#abba`) |
| TM-4 | `unary_div3.yaml` | `1^n`, n mod 3 = 0 ise kabul |

Tasarım ayrıntıları: [docs/design_notes.md](docs/design_notes.md). Üretim betikleri: `scripts/gen_*.py`.

## Test komutu

```bash
python -m pytest tests/ -q
```

## Sınırlamalar

- TM-1: n>255 ret; girdi yalnızca `1`.
- TM-2: Girdi biçimi `sol#sağ`; işaret sembolleri `r`,`s` şeritte kalır (kabul/ret kararı verilir).
- TM-3: Alfabe `{a,b}`; boş girdi ret.
- TM-4: Yalnızca unary `1`; boş girdi ret.

## Öğrenilenler

- Deterministik TM’de her `(durum, okunan)` tek geçiş olmalıdır.
- İkili karşılaştırmada sağ tarafın da işaretlenmesi gerekir; aksi halde her tur sağın MSB’si ile karşılaştırılır.
- Dize kopyada işaret (`X`) kopya bitene kadar silinmemelidir.
- `pytest` regresyonu, özellikle uzun YAML makinelerinde hatayı erken gösterir.

## Bonus (isteğe bağlı)

Çok şerit, NTM+BFS, adım grafiği, PPM/GIF: [docs/BONUS.md](docs/BONUS.md).

## Teslim notları

- Video: [docs/VIDEO_SUNUM.md](docs/VIDEO_SUNUM.md) ve `python scripts/demo_video.py --all`
- `final` etiketi öğrenci tarafından tamamlanmalıdır.
- GitHub `main` güncel tutulmalıdır.
