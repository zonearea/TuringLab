# TuringLab — günlük çalışma günlüğü

Proje ilerlemesinin kısa kaydı. Her gün için `## YYYY-MM-DD` başlığı altında **Planlanan**, **Yapılan**, **Test**, **Commit’ler**, **Yarın** ve **Not / blokaj** maddeleri doldurulur.

---
## 2026-05-11 — Proje iskeleti ve TM motoru

- **Planlanan:** Repo iskeleti; `turinglab` paketi; seyrek şerit + YAML doğrulama; `SingleTapeTM.run` iskeleti; ilk pytest; günlük dosyası.
- **Yapılan:**
  - Kök: [README.md](README.md), [requirements.txt](requirements.txt), [.gitignore](.gitignore), [pytest.ini](pytest.ini), [REPORT.md](REPORT.md) (taslak).
  - Motor: [turinglab/tm_engine.py](turinglab/tm_engine.py) — `SingleTapeTM`, `RunResult`, `TMStep`, YAML yükleme, `run` (accept / no_transition / timeout / reject), `verbose` çıktısı, seyrek `dict[int, str]` şerit ve negatif kafa indeksi.
  - Örnek makine: [machines/binary_increment.yaml](machines/binary_increment.yaml).
  - Testler: [tests/test_tm_engine.py](tests/test_tm_engine.py) (6 senaryo).
- **Test:** `python -m pytest tests/test_tm_engine.py -q` — 6 passed.
- **Commit’ler:** `91378ec` … `d3417ae` … arası docs commit’leri — tam liste: `git log --oneline`
- **Yarın:** Geçiş lookup / history ince ayarı; el kitabı örnek YAML’ları ekleme; test sayısını 8+ çıkarma.
- **Not / blokaj:** Yok.

---

## 2026-05-12 — Örnek makineler ve test genişletme

- **Planlanan:** El kitabı örnek makine YAML’ları; `test_tm_engine` 8+ test; rubrik kenarları (yinelenen geçiş, geçersiz girdi, `reject`); README ve günlük günceliği.
- **Yapılan:**
  - [machines/unary_increment.yaml](machines/unary_increment.yaml), [machines/even_a.yaml](machines/even_a.yaml), [machines/binary_palindrome.yaml](machines/binary_palindrome.yaml) eklendi (palindrom geçişleri Goldberg FCS örneğine göre, uyuşmazlık için `q_reject`).
  - [tests/test_tm_engine.py](tests/test_tm_engine.py): 12 test (`unary_increment`, `even_a`, `binary_palindrome`, geçersiz girdi `ValueError`, yinelenen δ `ValueError`, `TMStep` alan kontrolü).
  - [README.md](README.md): kurulum, makine tablosu, kaynak notu.
- **Test:** `python -m pytest tests/test_tm_engine.py -q` — 12 passed.
- **Commit’ler:** Tam liste: `git log --oneline`.
- **Yarın:** Bölüm 1 cilası (docstring / rubrik son kontrol); Bölüm 2 için `design_notes.md` taslağı veya TM-1 unary→binary tasarımına başlangıç.
- **Not / blokaj:** Yok.

---

## 2026-05-13 — Motor docstring ve README

- **Planlanan:** Bölüm 1 motor/docstring cilası; README Bölüm 1 bağımlılık notu; günlük kaydı; pytest yeşil.
- **Yapılan:**
  - [turinglab/tm_engine.py](turinglab/tm_engine.py): modül, ``TMStep``, ``RunResult``, ``SingleTapeTM`` (``__init__``, ``from_yaml``, ``run``) Google tarzı docstring; kullanılmayan ``typing`` importları temizlendi.
  - [turinglab/__init__.py](turinglab/__init__.py): paket docstring ve ``__all__`` açıklaması.
  - [README.md](README.md): Bölüm 1 izinli bağımlılıklar cümlesi.
- **Test:** `python -m pytest tests/test_tm_engine.py -q` — 12 passed.
- **Commit’ler:** `git log --oneline` ile bakılır.
- **Yarın:** TM-1 `unary_to_binary.yaml`, `tests/test_machines.py`, `docs/design_notes.md` (Bölüm 2).
- **Not / blokaj:** Yok.

---

## 2026-05-14 — TM-1 unary_to_binary ve test_machines

- **Planlanan:** TM-1 `unary_to_binary.yaml` doğrulama; `tests/test_machines.py`; `docs/design_notes.md`; README/günlük; pytest tam paket.
- **Yapılan:**
  - `unary_to_binary`: `q_rw1` ile X’e gelince unary tarafına `L`; `q_lr` sol baştaki `1` için doğrudan silme (`q_er`); `q_lr,X → q_cx` ile ayırıcı sonrası temizlik. Üretici: [scripts/gen_unary_to_binary.py](scripts/gen_unary_to_binary.py).
  - [tests/test_machines.py](tests/test_machines.py): yükleme, kabul (parametre: n∈{1,2,3,4,5,16,255}), boş ret, n=256 ret.
  - [docs/design_notes.md](docs/design_notes.md): TM-1 beş soru cevabı.
  - [README.md](README.md): `unary_to_binary` satırı ve `pytest tests/` komutu.
- **Test:** `python -m pytest tests/ -q` — 22 passed.
- **Commit’ler:** `git log --oneline` ile bakılır.
- **Yarın:** TM-1 manuel test tekrarı; el kitabı Bölüm 2 kapsamına bakış.
- **Not / blokaj:** Yok.

---

## 2026-05-15 — TM-1 doğrulama ve test tekrarı

- **Planlanan:** TM-1 sonrası doğrulama; `pytest` tam paket; `11`, `111`, `1111` örnekleri elle kontrol.
- **Yapılan:**
  - [machines/unary_to_binary.yaml](machines/unary_to_binary.yaml) ve [tests/test_machines.py](tests/test_machines.py) gözden geçirildi.
  - `python -m pytest tests/ -q` — 22 passed (o günkü durum).
  - El kitabı: Bölüm 2 rubriğinde TM-1 dışında ek makine istenip istenmediği not edildi (sonraki gün netleştirilecek).
- **Test:** `python -m pytest tests/ -q` — 22 passed.
- **Commit’ler:** Yok.
- **Yarın:** El kitabı Bölüm 2–3 sayfa kontrolü; `q0,0` ret ihtiyacı.
- **Not / blokaj:** Yok.

---

## 2026-05-16 — El kitabı Bölüm 2 kapsamı

- **Planlanan:** El kitabı Bölüm 2 kapsamı; TM-2/3 zorunluluğu; push durumu kontrolü.
- **Yapılan:**
  - Bölüm 2 özeti: ödev kapsamında **TM-1 (`unary_to_binary`)** tamam; ek TM yalnızca el kitabında açıkça istenirse.
  - GitHub: yerel `main` ile `origin/main` karşılaştırma planı (17 Mayıs’ta commit).
  - [docs/design_notes.md](docs/design_notes.md) okuma — kenar durumları listesi.
- **Test:** `python -m pytest tests/ -q` — 22 passed.
- **Commit’ler:** Yok.
- **Yarın:** `q0,0 → q_reject`, geçersiz girdi testi, `REPORT.md` taslağı.
- **Not / blokaj:** Yok.

---

## 2026-05-17 — Geçersiz girdi ret ve REPORT taslağı

- **Planlanan:** `q0,0 → q_reject`; geçersiz girdi testi; `REPORT.md` taslak; pytest.
- **Yapılan:**
  - [scripts/gen_unary_to_binary.py](scripts/gen_unary_to_binary.py): `q0` + `0` → `q_reject`; YAML yenilendi.
  - [tests/test_machines.py](tests/test_machines.py): `test_unary_to_binary_invalid_zero_reject`.
  - [docs/design_notes.md](docs/design_notes.md): kenar durumu güncellendi.
  - [REPORT.md](REPORT.md): Bölüm 3 mini-rapor taslağı (özet, Bölüm 1–2, sınırlar, teslim checklist).
- **Test:** `python -m pytest tests/ -q` — 23 passed.
- **Commit’ler:** `14037b8` — docs: REPORT taslak; unary_to_binary q0,0 ret.
- **Yarın:** `REPORT.md` bölüm tamamlama; teslim checklist.
- **Not / blokaj:** Yok.

---

## 2026-05-18 — REPORT gözden geçirme

- **Planlanan:** `REPORT.md` Bölüm 1–2 metinlerini gözden geçirme; teslim checklist; README’ye rapor linki planı.
- **Yapılan:**
  - [REPORT.md](REPORT.md): özet ve sınırlamalar okundu; teslim öncesi maddeler listelendi.
  - [docs/DAILY_LOG.md](docs/DAILY_LOG.md): 15–17 Mayıs girişleri yazıldı.
- **Test:** `python -m pytest tests/ -q` — 23 passed.
- **Commit’ler:** Yok.
- **Yarın:** `REPORT.md` öğrenilenler; README linkleri; push.
- **Not / blokaj:** Yok.

---

## 2026-05-19 — REPORT öğrenilenler ve README linkleri

- **Planlanan:** `REPORT.md` öğrenilenler bölümü; README’de rapor ve günlük linkleri; teslim planı; pytest + commit.
- **Yapılan:**
  - [REPORT.md](REPORT.md): “Öğrenilenler” bölümü; teslim checklist güncellendi.
  - [README.md](README.md): [REPORT.md](REPORT.md) ve [docs/DAILY_LOG.md](docs/DAILY_LOG.md) linkleri.
  - [docs/DAILY_LOG.md](docs/DAILY_LOG.md): 18–19 Mayıs girişleri; devam planı (teslim öncesi).
- **Test:** `python -m pytest tests/ -q` — 23 passed.
- **Commit’ler:** `b6f6744` — günlük başlıkları ve REPORT checklist.
- **Yarın:** Rubrik son kontrolü; video için `pytest -v` provası.
- **Not / blokaj:** Yok.

---

## 2026-05-20 — Rubrik ve REPORT son kontrol

- **Planlanan:** El kitabı Bölüm 1–3 rubrik; `REPORT.md` son okuma.
- **Yapılan:**
  - Bölüm 1–2 teslim maddeleri repoda mevcut (motor, örnek makineler, TM-1, testler).
  - [REPORT.md](REPORT.md): özet ve sınırlamalar son gözden geçirildi.
- **Test:** `python -m pytest tests/ -q` — 23 passed.
- **Commit’ler:** Yok.
- **Yarın:** Video çekimi; `pytest -v`; GitHub push doğrulama.
- **Not / blokaj:** Yok.

---

## 2026-05-21 — Test provası ve GitHub push

- **Planlanan:** `pytest tests/ -v` (video); günlük 20–21; `git push origin main`.
- **Yapılan:**
  - Tam test paketi çalıştırıldı (video için komut hazır).
  - [docs/DAILY_LOG.md](docs/DAILY_LOG.md): 20–21 Mayıs girişleri.
- **Test:** `python -m pytest tests/ -q` — 23 passed.
- **Commit’ler:** Bu oturum — günlük 20–21.
- **Yarın:** Video yükleme / teslim (hoca talimatına göre).
- **Not / blokaj:** Yok.
