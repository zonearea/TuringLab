# turinglab-HüseyinBerkayKayıkçı

[TuringLab_Ogrenci_ElKitabi.pdf](https://github.com/user-attachments/files/27605487/TuringLab_Ogrenci_ElKitabi.pdf)

Selçuk Üniversitesi Hesaplama Kuramı — **TuringLab** final ödevi: tek şeritli deterministik TM motoru (YAML), örnek makineler ve pytest.

- Mini-rapor: [REPORT.md](REPORT.md)
- Günlük: [docs/DAILY_LOG.md](docs/DAILY_LOG.md)
- **Video sunum:** [docs/VIDEO_SUNUM.md](docs/VIDEO_SUNUM.md) — metin, komutlar, beklenen çıktılar
- Bonus modüller: [docs/BONUS.md](docs/BONUS.md) (`pip install -r requirements-bonus.txt`)

## Gereksinimler

- Python 3.10+
- `pip install -r requirements.txt`

**Bölüm 1 (el kitabı):** Üçüncü parti yalnızca **PyYAML** ve **pytest**; standart kütüphane serbest.

## Test

```bash
python -m pytest tests/ -q
```

Ayrıntılı çıktı (demo / video):

```bash
python -m pytest tests/ -v
```

Video kaydı için terminal demoları (Bölüm 1–8):

```powershell
chcp 65001
python scripts/demo_video.py --all
# veya: .\scripts\run_video_demo.ps1
```

Tek bölüm: `python scripts/demo_video.py --section 3` (TM-1 verbose). Ayrıntı: [docs/VIDEO_SUNUM.md](docs/VIDEO_SUNUM.md).

Tüm testler yeşil olmalı (Bölüm 1 rubriği: en az 8 test; Bölüm 2’de `test_machines.py` eklenir).

## Örnek makineler (`machines/`)

| Dosya | Kısa açıklama |
|--------|----------------|
| [machines/binary_increment.yaml](machines/binary_increment.yaml) | İkili sayı +1 (el kitabı örneği) |
| [machines/unary_increment.yaml](machines/unary_increment.yaml) | Unary `1^n` → `1^(n+1)` |
| [machines/even_a.yaml](machines/even_a.yaml) | `{a,b}` üzerinde çift sayıda `a` |
| [machines/binary_palindrome.yaml](machines/binary_palindrome.yaml) | `{0,1}` palindrom (geçişler Paul Goldberg [FCS örneği](http://www.cs.ox.ac.uk/people/paul.goldberg/FCS/tm1.html) tabanı; uyuşmazlıkta `q_reject`) |
| [machines/unary_to_binary.yaml](machines/unary_to_binary.yaml) | Unary `1^n` → n’nin ikili yazımı (K=8 bit alan; n≤255) |
| [machines/binary_compare.yaml](machines/binary_compare.yaml) | `sol#sag` — sol ikili > sağ ikili ise kabul |
| [machines/string_copy.yaml](machines/string_copy.yaml) | `w` → `w#w` (`{a,b}`) |
| [machines/unary_div3.yaml](machines/unary_div3.yaml) | `1^n`, n mod 3 = 0 ise kabul |

Bölüm 2 tasarım notları: [docs/design_notes.md](docs/design_notes.md).

Ders sayfasında farklı YAML verilmişse, aynı şema ile `machines/` altına kopyalanıp testlere bağlanabilir.

## Şerit ve sol taşma

Şerit seyrek `dict[int, str]` ile tutulur; kafa indeksi negatif olabilir. Sol uçta okuma yeni `blank` hücreleri oluşturur (davranış [turinglab/tm_engine.py](turinglab/tm_engine.py) + bu README ile sabitlenir).

## GitHub

Remote ekli değilse:

```bash
git remote add origin <repo-URL>
git push -u origin main
```

(Dal adın `master` ise son satırda `master` kullan.)
